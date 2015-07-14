# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import event.models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_auto_20150714_0411'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=event.models.event_images)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='image',
        ),
        migrations.AddField(
            model_name='eventimage',
            name='event',
            field=models.ForeignKey(related_name='images', to='event.Event'),
        ),
    ]
