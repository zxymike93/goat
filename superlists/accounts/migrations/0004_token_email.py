# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='email',
            field=models.EmailField(max_length=254, default='a@b.c'),
            preserve_default=False,
        ),
    ]
