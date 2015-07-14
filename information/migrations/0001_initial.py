# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'logos', blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('facebook', models.URLField(null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('fax', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'logos', blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('facebook', models.URLField(null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('fax', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'logos', blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('facebook', models.URLField(null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('fax', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmergencyContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=256)),
                ('description', models.TextField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'logos', blank=True)),
                ('link', models.URLField(null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('facebook', models.URLField(null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('fax', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
