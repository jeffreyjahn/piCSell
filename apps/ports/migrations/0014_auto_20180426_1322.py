# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 20:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0013_auto_20180426_1251'),
    ]

    operations = [
        migrations.RenameField(
            model_name='photo',
            old_name='url',
            new_name='image',
        ),
    ]
