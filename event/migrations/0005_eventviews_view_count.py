# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20150714_0522'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventviews',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
