# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
        ('country', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatDescription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('description', models.TextField()),
                ('narrative', models.TextField(null=True, blank=True)),
                ('code', models.SlugField()),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('value', models.DecimalField(null=True, max_digits=20, decimal_places=10, blank=True)),
                ('visible', models.BooleanField(default=True)),
                ('country', models.ForeignKey(to='country.Country')),
                ('description', models.ForeignKey(to='stats.StatDescription')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='statvalue',
            unique_together=set([('description', 'country', 'year')]),
        ),
        migrations.AddField(
            model_name='statdescription',
            name='group',
            field=adminsortable.fields.SortableForeignKey(to='stats.StatGroup'),
            preserve_default=True,
        ),
    ]
