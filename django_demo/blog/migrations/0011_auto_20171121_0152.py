# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 22:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_postfile_is_removed'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(max_length=50)),
                ('storage', models.CharField(max_length=1500)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Post')),
            ],
        ),
        migrations.AddField(
            model_name='postquestion',
            name='block',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='blog.PostBlock'),
            preserve_default=False,
        ),
    ]