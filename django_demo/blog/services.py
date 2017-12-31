from .helpers import Request
from django.utils.timezone import now

from . import models
from . import helpers


def unpack_and_save_all_blocks(request, post_id: int):
    text_blocks, code_blocks = Request.get_list_fields_request(request, 'text_block', 'code_block')
    for block in text_blocks:
        models.PostBlock(block_type=models.PostBlock.BLOCK_TEXT, storage=block, post_id=post_id).save()

    for block in code_blocks:
        models.PostBlock(block_type=models.PostBlock.BLOCK_CODE, storage=block, post_id=post_id).save()

    for image in request.FILES.getlist(key='image_block'):
        file_name = helpers.File.get_valid_name(image)
        models.PostFile(post_id=post_id, file_type=models.PostFile.LOCAL_IMAGE, file_name=file_name,
                        created_at=now()).save()
        models.PostBlock(post_id=post_id, block_type=models.PostBlock.BLOCK_IMAGE, storage=file_name).save()
        helpers.File.save(image, file_name)
