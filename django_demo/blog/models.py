from django.db import models
from django.contrib.auth.models import User
from os import remove
from django.conf import settings


class Feedback(models.Model):
    name = models.CharField(max_length=50, help_text='Ваше имя')
    email = models.EmailField(help_text='Ваш email')
    question = models.CharField(max_length=1500, help_text='Вопрос')
    created_at = models.DateTimeField()
    is_read = models.BooleanField(default=False)
    user_ip = models.CharField(max_length=50)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    post_text = models.CharField(max_length=5000)
    created_at = models.DateTimeField()
    is_removed = models.BooleanField(default=False)

    def have_post_image(self):
        return self.postfile_set.filter(file_type=PostFile.POST_IMAGE).exists()

    def get_post_image_name(self):
        return self.postfile_set.filter(file_type=PostFile.POST_IMAGE).first().file_name

    def __str__(self):
        return "{id} | {author} : {title}".format(id=self.id, author=self.user.username, title=self.title)


class PostFile(models.Model):
    POST_IMAGE = 'post_image'
    LOCAL_IMAGE = 'local_image'
    REMOTE_IMAGE = 'remote_image'

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=150)
    file_type = models.CharField(max_length=50)
    file_description = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField()

    def __str__(self):
        return "{id} | {type} : {filename}".format(id=self.id, type=self.file_type, filename=self.file_name)

    def delete(self, using=None, keep_parents=False):
        remove(settings.BASE_DIR + 'blog/static/blog/user_files' + self.file_name)
        super(PostFile, self).delete()


class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=500)
    created_at = models.DateTimeField()

    def __str__(self):
        return "{id} | {user} : {text}".format(id=self.id, user=self.user.username, text=self.comment_text)


class PostQuestion(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)

    def __str__(self):
        return "{id} | {post_title} : {text}".format(id=self.id, post_title=self.post.title, text=self.question_text)


class PostQuestionChoice(models.Model):
    question = models.ForeignKey(PostQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=150)
    choice_votes = models.IntegerField(default=0)

    def __str__(self):
        return "{id} | {ques} : {text}".format(id=self.id, ques=self.question.question_text, text=self.choice_text)
