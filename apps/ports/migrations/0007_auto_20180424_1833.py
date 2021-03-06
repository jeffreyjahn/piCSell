# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-25 01:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ports', '0006_auto_20180424_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_1', models.CharField(max_length=128)),
                ('address_2', models.CharField(max_length=128, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_on', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='photo',
            name='tags',
        ),
        migrations.AlterField(
            model_name='comment',
            name='photo_commented',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ports.Photo'),
        ),
        migrations.AlterField(
            model_name='photo',
            name='likers',
            field=models.ManyToManyField(null=True, related_name='liked_photos', to='ports.User'),
        ),
        migrations.AddField(
            model_name='tag',
            name='tagged_photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='ports.Photo'),
        ),
    ]
