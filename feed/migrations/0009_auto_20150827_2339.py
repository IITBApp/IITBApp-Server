# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_feedentry_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=128, db_index=True)),
                ('scheme', models.URLField(null=True, blank=True)),
                ('label', models.CharField(max_length=128, null=True, blank=True)),
                ('feed_config', models.ForeignKey(to='feed.FeedConfig')),
            ],
        ),
        migrations.AddField(
            model_name='feedentry',
            name='categories',
            field=models.ManyToManyField(to='feed.FeedCategory'),
        ),
        migrations.AlterUniqueTogether(
            name='feedcategory',
            unique_together=set([('feed_config', 'term')]),
        ),
    ]
