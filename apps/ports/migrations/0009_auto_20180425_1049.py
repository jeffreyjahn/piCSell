# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-25 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0008_auto_20180424_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='user_addresses',
            field=models.ManyToManyField(related_name='addresses', to='ports.User'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='description',
            field=models.TextField(max_length=500, null=True),
        ),
    ]
