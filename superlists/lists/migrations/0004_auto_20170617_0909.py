# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20170617_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='list',
            field=models.ForeignKey(default=None, to='lists.List'),
        ),
    ]
