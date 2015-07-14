# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0002_notice_posted_by'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notice',
            old_name='issue_date',
            new_name='time',
        ),
    ]
