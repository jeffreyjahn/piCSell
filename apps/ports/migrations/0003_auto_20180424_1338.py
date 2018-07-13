# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-24 20:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0002_auto_20180424_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='likers',
            field=models.ManyToManyField(related_name='liked_photos', to='ports.User'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='uploader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_photos', to='ports.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='modified_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
