from django import template
import re

register = template.Library()


@register.filter()
def code_wrapper(string):
    return re.sub(r'```(.*?)```', r'<code>\1</code>', string, flags=re.S | re.M)
