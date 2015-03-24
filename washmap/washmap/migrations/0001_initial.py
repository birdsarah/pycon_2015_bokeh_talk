# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('visible', models.IntegerField(null=True, blank=True)),
                ('currency_name', models.CharField(blank=True, max_length=40)),
                ('last_contributor_id', models.IntegerField(null=True, blank=True)),
                ('last_contributed_on', models.DateTimeField(null=True, blank=True)),
                ('last_contributed_sector', models.CharField(blank=True, max_length=255)),
                ('country_meta', django_countries.fields.CountryField(null=True, blank=True, max_length=2)),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['slug'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('local_name', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(to='washmap.Country', null=True, editable=False, related_name='translations')),
            ],
            options={
                'db_table': 'washmap_country_translation',
                'abstract': False,
                'managed': True,
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('water_declaration', models.CharField(blank=True, max_length=255)),
                ('sanitation_declaration', models.CharField(blank=True, max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('coords', models.TextField(blank=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegionTranslation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('local_name', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(to='washmap.Region', null=True, editable=False, related_name='translations')),
            ],
            options={
                'db_table': 'washmap_region_translation',
                'abstract': False,
                'managed': True,
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WASHMapData',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('sanitation_increase', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('sanitation_initial', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('sanitation_pop_current', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('sanitation_pop_universal', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('water_increase', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('water_initial', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('water_pop_current', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('water_pop_universal', models.DecimalField(null=True, blank=True, decimal_places=5, max_digits=20)),
                ('country', models.ForeignKey(to='washmap.Country')),
            ],
            options={
                'verbose_name_plural': 'WASHMap Data',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='regiontranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='countrytranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(to='washmap.Region', null=True, blank=True),
            preserve_default=True,
        ),
    ]
