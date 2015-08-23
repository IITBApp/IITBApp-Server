# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugtracker',
            name='posted_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 23, 7, 47, 37, 491411, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
