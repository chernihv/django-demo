from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import resolve_url, render, get_object_or_404
from django.utils import timezone

from .. import constants, models, helpers, decorators, forms, services
from ..helpers import is_post, get_valid_name, save_file, go_home, redirect


@decorators.group_require(constants.Group.REGULAR_USER)
def post_create(request):
    if is_post(request):
        form = forms.PostForm(request.POST)
        image_form = forms.PostFileForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.user = request.user
            post.save()
            services.unpack_and_save_all_blocks(request, post.id)
            if image_form.is_valid():
                file = request.FILES['file']
                saved_name = get_valid_name(file)
                save_file(file, saved_name)
                models.PostFile(post_id=post.id, file_type=models.PostFile.POST_IMAGE,
                                file_name=saved_name, created_at=timezone.now()).save()
            return JsonResponse({'redirect': resolve_url('blog:detail', post.id)})
    else:
        post = models.Post.get_post_or_create(request.user.id)
        form = forms.PostForm(instance=post)
        image_form = forms.PostFileForm()
    return render(request, 'blog/post_create.html', {'form': form, 'image_form': image_form})


@decorators.group_require(constants.Group.REGULAR_USER)
def post_edit(request, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    form = forms.PostForm(instance=post)
    image_form = forms.PostFileForm()
    if request.user.id == post.user_id:
        if is_post(request):
            form = forms.PostForm(request.POST, instance=post)
            image_form = forms.PostFileForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                services.unpack_and_save_all_blocks(request, post_id)
                if image_form.is_valid():
                    post.disable_post_image()
                    file = request.FILES['file']
                    saved_name = get_valid_name(file)
                    save_file(file, saved_name)
                    models.PostFile(post_id=post.id, file_type=models.PostFile.POST_IMAGE,
                                    file_name=saved_name, created_at=timezone.now()).save()
            return JsonResponse({'redirect': resolve_url('blog:detail', post.id)})
        else:
            return render(request, 'blog/post_edit.html', {'form': form, 'image_form': image_form})
    else:
        return HttpResponseForbidden()


@decorators.group_require(constants.Group.REGULAR_USER)
def post_delete(request, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    if request.user.id == post.user_id:
        post.remove_post()
        return go_home()
    else:
        return HttpResponseForbidden()


@decorators.group_require(constants.Group.REGULAR_USER)
def publish_post(request, post_id: int):
    post = get_object_or_404(models.Post, pk=post_id, is_removed=False)
    if request.user.id != post.user_id:
        return HttpResponseForbidden()
    models.PostBlock.publish_all_blocks(post_id)
    post.publish_post()
    return JsonResponse({'redirect': resolve_url('blog:detail', post_id)})


@decorators.group_require(constants.Group.REGULAR_USER)
def block_create(request, post_id: int):
    post = get_object_or_404(models.Post, pk=post_id, is_removed=False)
    if request.user.id != post.user_id:
        return HttpResponseForbidden()
    block = models.PostBlock(post_id=post_id, is_published=False)
    if request.POST.get('block_type') == models.PostBlock.BLOCK_CODE:
        block.block_type = models.PostBlock.BLOCK_CODE
    elif request.POST.get('block_type') == models.PostBlock.BLOCK_TEXT:
        block.block_type = models.PostBlock.BLOCK_TEXT
    elif request.POST.get('block_type') == models.PostBlock.BLOCK_IMAGE:
        block.block_type = models.PostBlock.BLOCK_IMAGE
    else:
        return HttpResponseBadRequest('Not valid block type')
    block.save()
    return JsonResponse({'block_id': block.id, 'block_type': block.block_type})


@decorators.group_require(constants.Group.REGULAR_USER)
def block_save(request, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    if request.user.id != post.user_id:
        return HttpResponseForbidden()
    block_id = request.POST.get('block_id')
    block = models.PostBlock.objects.get(pk=block_id)
    block.storage = request.POST.get('value')
    block.save()
    return JsonResponse({'status': '200', 'block_id': block.id})


@decorators.group_require(constants.Group.REGULAR_USER)
def block_delete(request, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    if request.user.id == post.user_id:
        block_id = request.POST.get('block_id')
        models.PostBlock.get_block_or_404(block_id).hide()
        return JsonResponse({'status': '200', 'block_id': block_id})
    else:
        return HttpResponseForbidden()


def post_detail(request, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    return render(request, 'blog/post_detail.html', {'post': post})


@decorators.group_require(constants.Group.REGULAR_USER)
def post_remove_header_image(request, post_id: int):
    post = models.Post.get_post_or_404(post_id)
    post.disable_post_image()
    return redirect('blog:edit', args=[post_id])


@decorators.group_require(constants.Group.REGULAR_USER)
def post_comment(request, post_id: int):
    if is_post(request):
        comment_text = request.POST['post_comment']
        models.PostComment(post_id=post_id, comment_text=comment_text, created_at=timezone.now(),
                           user_id=request.user.id).save()
        return redirect('blog:detail', args=[post_id])


@decorators.superuser_only
def post_comment_hide(request, comment_id: int):
    comment = get_object_or_404(models.PostComment, pk=comment_id)
    comment.hide_comment()
    return redirect('blog:detail', args=[comment.post_id])
