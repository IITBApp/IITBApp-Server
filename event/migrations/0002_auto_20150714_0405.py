# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='created',
            new_name='time',
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(null=True, upload_to=event.models.event_images, blank=True),
        ),
    ]
