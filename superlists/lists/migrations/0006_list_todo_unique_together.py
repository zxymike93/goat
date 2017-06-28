# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_auto_20170624_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='task',
            field=models.TextField(default=''),
        ),
        migrations.AlterUniqueTogether(
            name='todo',
            unique_together=set([('list', 'task')]),
        ),
    ]
