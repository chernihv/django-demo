from django.contrib import admin
from . import models


class ChoiceInLine(admin.TabularInline):
    model = models.Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date info', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    search_fields = ['question_text']


admin.site.register(models.Question, QuestionAdmin)
