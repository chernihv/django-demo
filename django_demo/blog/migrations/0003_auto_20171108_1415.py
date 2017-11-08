# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-08 11:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_postcomment_postfile_postquestion_postquestionchoice'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postcomment',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='postfile',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postquestion',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='postquestionchoice',
            old_name='question_id',
            new_name='question',
        ),
    ]
