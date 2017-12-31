from django import template
from ..models import Post
import re

register = template.Library()


@register.filter()
def code_wrapper(string):
    return re.sub(r'```(.*?)```', r'<code>\1</code>', string, flags=re.S | re.M)


@register.simple_tag
def get_objects():
    return Post.get_all_active_posts()
