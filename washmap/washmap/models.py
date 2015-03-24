from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.db import models

from hvad.models import TranslatableModel, TranslatedFields
from django_countries.fields import CountryField


class Region(TranslatableModel):
    translations = TranslatedFields(
        local_name=models.CharField(max_length=255)
    )
    name = models.CharField(max_length=255)
    water_declaration = models.CharField(max_length=255, blank=True)
    sanitation_declaration = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    coords = models.TextField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name


class Country(TranslatableModel):

    class Meta:
        verbose_name_plural = 'Countries'
        ordering = ['slug']

    translations = TranslatedFields(
        local_name=models.CharField(max_length=255)
    )
    region = models.ForeignKey(Region, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    visible = models.IntegerField(null=True, blank=True)
    currency_name = models.CharField(max_length=40, blank=True)
    last_contributor_id = models.IntegerField(null=True, blank=True)
    last_contributed_on = models.DateTimeField(null=True, blank=True)
    last_contributed_sector = models.CharField(max_length=255, blank=True)
    country_meta = CountryField(null=True, blank=True)

    @property
    def code(self):
        return self.country_meta.code

    def __unicode__(self):
        return self.local_name

    def get_absolute_url(self):
        return reverse('country-comparison', kwargs={'country': self.slug})


class WASHMapData(models.Model):
    class Meta:
        verbose_name_plural = "WASHMap Data"

    country = models.ForeignKey(Country)
    decimal_field_props = dict(
        max_digits=20, decimal_places=5, null=True, blank=True
    )
    sanitation_increase = models.DecimalField(**decimal_field_props)
    sanitation_initial = models.DecimalField(**decimal_field_props)
    sanitation_pop_current = models.DecimalField(**decimal_field_props)
    sanitation_pop_universal = models.DecimalField(**decimal_field_props)
    water_increase = models.DecimalField(**decimal_field_props)
    water_initial = models.DecimalField(**decimal_field_props)
    water_pop_current = models.DecimalField(**decimal_field_props)
    water_pop_universal = models.DecimalField(**decimal_field_props)

    def __unicode__(self):
        return u'%s' % self.country
