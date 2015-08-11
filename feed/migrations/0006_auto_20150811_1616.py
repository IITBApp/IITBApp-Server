# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0005_feedconfig_feedentry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedconfig',
            name='last_checked',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 5, 30, tzinfo=utc), null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='feedconfig',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]
