from django.contrib import admin
from .models.questions import Questions, Choice
from .models.posts import Post

admin.site.register(Post)
admin.site.register(Questions)
admin.site.register(Choice)
