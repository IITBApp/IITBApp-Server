# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20150726_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 31, 15, 8, 44, 450651, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usertoken',
            name='last_accessed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
