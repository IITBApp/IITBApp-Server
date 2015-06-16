# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='last_modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 16, 16, 55, 45, 717795), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='registration',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
    ]
