# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0004_feedview_view_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('etag', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('title', models.CharField(max_length=128, null=True, blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('check_frequency', models.IntegerField(default=30)),
                ('last_checked', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FeedEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_id', models.CharField(max_length=200, db_index=True)),
                ('title', models.CharField(max_length=128)),
                ('link', models.URLField()),
                ('updated', models.DateTimeField()),
                ('published', models.DateTimeField()),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=64)),
                ('feed_config', models.ForeignKey(related_name='entries', to='feed.FeedConfig')),
            ],
        ),
    ]
