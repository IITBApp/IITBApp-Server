# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0003_auto_20150804_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedview',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
