# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20150703_1916'),
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='posted_by',
            field=models.ForeignKey(default=None, to='authentication.Designation'),
            preserve_default=False,
        ),
    ]
