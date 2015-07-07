# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import event.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authentication', '0004_auto_20150703_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=16, choices=[(b'sport', b'SPORTS')])),
                ('event_time', models.DateTimeField()),
                ('event_place', models.CharField(max_length=256)),
                ('image', models.ImageField(null=True, upload_to=event.models.event_images)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cancelled', models.BooleanField(default=False)),
                ('posted_by', models.ForeignKey(related_name='events', to='authentication.Designation')),
            ],
        ),
        migrations.CreateModel(
            name='EventLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(related_name='likes', to='event.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventViews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(related_name='views', to='event.Event')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
