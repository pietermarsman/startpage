# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 22:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_auto_20171128_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('human_readable_text', models.TextField(max_length=128)),
                ('computer_readable_text', models.TextField(default='error', max_length=128, unique=True)),
                ('priority', models.PositiveIntegerField(default=0)),
                ('timer_running', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='todo',
            name='state',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='todo.TodoState'),
            preserve_default=False,
        ),
    ]
