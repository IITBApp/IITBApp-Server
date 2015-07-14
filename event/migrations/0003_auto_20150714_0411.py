# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20150714_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.CharField(max_length=16, choices=[(b'music', b'Music'), (b'photo', b'Photography'), (b'art', b'Fine Arts'), (b'sports', b'Sports'), (b'activity', b'Activity'), (b'tech', b'Tech'), (b'food', b'Food'), (b'literature', b'Literature')]),
        ),
    ]
