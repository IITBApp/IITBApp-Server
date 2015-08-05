# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_auto_20150718_0611'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsviews',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
    ]
