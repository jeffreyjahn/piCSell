# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-08-02 23:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0033_auto_20180801_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
