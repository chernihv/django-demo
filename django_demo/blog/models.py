from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
    name = models.CharField(max_length=50, help_text='Ваше имя')
    email = models.EmailField(help_text='Ваш email')
    question = models.CharField(max_length=1500, help_text='Вопрос')
    created_at = models.DateTimeField()
    user_ip = models.CharField(max_length=50)


class Post(models.Model):
    user_id = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    post_text = models.CharField(max_length=5000)
    created_at = models.DateTimeField()


class PostFile(models.Model):
    post_id = models.ForeignKey(Post)
    file_name = models.CharField(max_length=150)
    file_type = models.CharField(max_length=50)
    file_description = models.CharField(max_length=150)
    created_at = models.DateTimeField()


class PostComment(models.Model):
    post_id = models.ForeignKey(Post)
    user_id = models.IntegerField()
    comment_text = models.CharField(max_length=500)
    created_at = models.DateTimeField()


class PostQuestion(models.Model):
    post_id = models.ForeignKey(Post)
    question_text = models.CharField(max_length=500)


class PostQuestionChoice(models.Model):
    question_id = models.ForeignKey(PostQuestion)
    choice_text = models.CharField(max_length=150)
    choice_votes = models.IntegerField()
