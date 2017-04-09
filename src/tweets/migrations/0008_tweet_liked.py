# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-09 20:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tweets', '0007_tweet_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweet',
            name='liked',
            field=models.ManyToManyField(blank=True, related_name='liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
