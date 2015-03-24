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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('visible', models.IntegerField(null=True, blank=True)),
                ('currency_name', models.CharField(max_length=40, blank=True)),
                ('last_contributor_id', models.IntegerField(null=True, blank=True)),
                ('last_contributed_on', models.DateTimeField(null=True, blank=True)),
                ('last_contributed_sector', models.CharField(max_length=255, blank=True)),
                ('country_meta', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
            ],
            options={
                'ordering': ['slug'],
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_name', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='country.Country', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'country_country_translation',
                'db_tablespace': '',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('water_declaration', models.CharField(max_length=255, blank=True)),
                ('sanitation_declaration', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('created_at', models.DateTimeField(null=True, blank=True)),
                ('updated_at', models.DateTimeField(null=True, blank=True)),
                ('coords', models.TextField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegionTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('local_name', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='country.Region', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'country_region_translation',
                'db_tablespace': '',
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
            field=models.ForeignKey(blank=True, to='country.Region', null=True),
            preserve_default=True,
        ),
    ]
