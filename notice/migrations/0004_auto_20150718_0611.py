# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0003_auto_20150714_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='expiration_date',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
