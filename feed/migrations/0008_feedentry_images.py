# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0007_feedentrylike_feedentryview'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedentry',
            name='images',
            field=models.TextField(null=True, blank=True),
        ),
    ]
