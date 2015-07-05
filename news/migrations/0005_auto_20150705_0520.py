# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_news_published'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='posted_by',
            field=models.ForeignKey(related_name='news', to='authentication.Designation'),
        ),
    ]
