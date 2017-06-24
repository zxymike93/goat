# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_auto_20170617_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='task',
            field=models.TextField(),
        ),
    ]
