# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20150731_2038'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertoken',
            name='has_expired',
            field=models.BooleanField(default=False),
        ),
    ]
