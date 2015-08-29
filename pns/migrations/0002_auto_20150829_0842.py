# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pns', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='reg_id',
            field=models.CharField(max_length=256, verbose_name=b'Registration Id'),
        ),
    ]
