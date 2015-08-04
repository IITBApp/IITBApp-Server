# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeedLike',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FeedView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(max_length=128)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='feed',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='feed',
            name='user',
        ),
        migrations.DeleteModel(
            name='Feed',
        ),
        migrations.AlterUniqueTogether(
            name='feedview',
            unique_together=set([('guid', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='feedlike',
            unique_together=set([('guid', 'user')]),
        ),
    ]
