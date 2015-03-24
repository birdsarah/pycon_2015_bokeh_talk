# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0003_auto_20150324_0618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='boundary',
            field=models.TextField(help_text='A geojson representation of the geographical boundary', blank=True),
            preserve_default=True,
        ),
    ]
