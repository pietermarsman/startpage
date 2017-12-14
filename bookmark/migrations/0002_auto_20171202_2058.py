# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 20:58
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('bookmark', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmark',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks',
                                    to='bookmark.Label'),
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='name',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='label',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]