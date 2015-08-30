# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0009_auto_20150827_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedcategory',
            name='subscribers',
            field=models.ManyToManyField(related_name='feed_subscriptions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feedcategory',
            name='feed_config',
            field=models.ForeignKey(related_name='categories', to='feed.FeedConfig'),
        ),
        migrations.AlterField(
            model_name='feedentry',
            name='categories',
            field=models.ManyToManyField(related_name='entries', to='feed.FeedCategory'),
        ),
    ]
