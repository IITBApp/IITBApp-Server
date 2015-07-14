# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('priority', models.CharField(max_length=1, choices=[(b'0', b'Low'), (b'1', b'Medium'), (b'2', b'High'), (b'3', b'Urgent')])),
                ('expiration_date', models.DateTimeField(null=True)),
            ],
        ),
    ]
