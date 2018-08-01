# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-01 23:14
from __future__ import unicode_literals

import apps.ports.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0032_auto_20180731_1401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=apps.ports.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(upload_to=apps.ports.models.user_directory_path_profile),
        ),
    ]