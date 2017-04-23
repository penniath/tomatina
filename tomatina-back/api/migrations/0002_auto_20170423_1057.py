# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-23 10:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pomodoro',
            options={'ordering': ('-started',)},
        ),
        migrations.AlterField(
            model_name='pomodoro',
            name='started',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 23, 10, 57, 18, 413827, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='pomodoro',
            unique_together=set([]),
        ),
    ]
