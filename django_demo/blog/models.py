from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone


class Feedback(models.Model):
    name = models.CharField(max_length=50, help_text='Ваше имя')
    email = models.EmailField(help_text='Ваш email')
    question = models.CharField(max_length=1500, help_text='Вопрос')
    created_at = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    user_ip = models.CharField(max_length=50)

    @staticmethod
    def get_valid_questions():
        return Feedback.objects.filter(is_read=False)

    @staticmethod
    def hide_question(q_id: int):
        question = Feedback.objects.get(pk=q_id)
        question.is_read = True
        question.save()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=True)
    post_text = models.CharField(max_length=5000, null=True)
    created_at = models.DateTimeField()
    is_removed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    @staticmethod
    def get_post_or_create(user_id: int):
        try:
            post = Post.objects.get(user_id=user_id, is_published=False, is_removed=False)
        except Post.DoesNotExist:
            post = Post(user_id=user_id, is_published=False, created_at=timezone.now())
            post.save()
        return post

    @staticmethod
    def get_all_active_posts():
        return Post.objects.filter(is_removed=False, is_published=True).order_by('-created_at')

    @staticmethod
    def get_post_or_404(post_id: int):
        return get_object_or_404(Post, pk=post_id, is_removed=False, is_published=True)

    def get_valid_comments(self):
        return PostComment.get_valid_comments(self.id)

    def get_all_blocks(self):
        return PostBlock.get_all_valid_blocks(self.id).order_by('pk')

    def get_unpublished_blocs(self):
        return PostBlock.get_unpublished_blocks(self.id).order_by('pk')

    def remove_post(self):
        self.is_removed = True
        self.save()

    def have_post_image(self):
        return self.postfile_set.filter(file_type=PostFile.POST_IMAGE, is_removed=False).exists()

    def have_post_block(self):
        return self.postblock_set.filter(is_removed=False).exists()

    def get_post_image(self):
        return self.postfile_set.get(file_type=PostFile.POST_IMAGE, is_removed=False)

    def disable_post_image(self):
        post_image = self.get_post_image()
        if post_image is not None:
            post_image.is_removed = True
            post_image.save()

    def __str__(self):
        return "{id} | {author} : {title}".format(id=self.id, author=self.user.username, title=self.title)


class PostBlock(models.Model):
    BLOCK_IMAGE = 'block_image'
    BLOCK_CODE = 'block_code'
    BLOCK_TEXT = 'block_text'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    block_type = models.CharField(max_length=50)
    storage = models.CharField(max_length=1500, null=True)
    is_removed = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)

    @staticmethod
    def get_all_valid_blocks(post_id: int):
        return PostBlock.objects.filter(post_id=post_id, is_removed=False, is_published=True)

    @staticmethod
    def get_block_or_404(block_id):
        return get_object_or_404(PostBlock, pk=block_id, is_removed=False)

    @staticmethod
    def get_unpublished_blocks(post_id: int):
        return PostBlock.objects.filter(post_id=post_id, is_removed=False, is_published=False)

    def hide(self):
        self.is_removed = True
        self.save()


class PostFile(models.Model):
    POST_IMAGE = 'post_image'
    LOCAL_IMAGE = 'local_image'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=150)
    file_type = models.CharField(max_length=50)
    file_description = models.CharField(max_length=150, null=True, blank=True)
    is_removed = models.BooleanField(default=False)
    created_at = models.DateTimeField()

    def __str__(self):
        return "{id} | {type} : {filename}".format(id=self.id, type=self.file_type, filename=self.file_name)


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    is_removed = models.BooleanField(default=False)

    @staticmethod
    def get_valid_comments(post_id=None):
        return PostComment.objects.filter(is_removed=False, post_id=post_id)

    def hide_comment(self):
        self.is_removed = True
        self.save()

    def __str__(self):
        return "{id} | {user} : {text}".format(id=self.id, user=self.user.username, text=self.comment_text)
