# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_designation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='designation',
            old_name='designation_name',
            new_name='post',
        ),
    ]
