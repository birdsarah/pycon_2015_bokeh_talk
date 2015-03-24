# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0002_country_boundary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='boundary',
            field=models.TextField(help_text='A geojson representation of the geographical boundary', editable=False, blank=True),
            preserve_default=True,
        ),
    ]
