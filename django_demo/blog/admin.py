from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Post)
admin.site.register(models.Feedback)
admin.site.register(models.PostFile)
admin.site.register(models.PostComment)
