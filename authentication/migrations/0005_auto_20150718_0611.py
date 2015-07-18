# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20150703_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='designation',
            name='user',
            field=models.ForeignKey(related_name='designations', to=settings.AUTH_USER_MODEL),
        ),
    ]
