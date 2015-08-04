# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0002_auto_20150804_2220'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedlike',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='feedview',
            unique_together=set([]),
        ),
    ]
