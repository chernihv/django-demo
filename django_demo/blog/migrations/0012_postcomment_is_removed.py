# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 23:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20171121_0152'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcomment',
            name='is_removed',
            field=models.BooleanField(default=False),
        ),
    ]
