# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statdescription',
            name='group',
        ),
        migrations.DeleteModel(
            name='StatGroup',
        ),
        migrations.RemoveField(
            model_name='statdescription',
            name='narrative',
        ),
        migrations.RemoveField(
            model_name='statvalue',
            name='visible',
        ),
    ]
