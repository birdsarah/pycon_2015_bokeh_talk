from __future__ import absolute_import, unicode_literals

from django.contrib import admin

from .models import (
    Country,
    Region,
    WASHMapData,
)

from hvad.admin import TranslatableAdmin


class CountryAdmin(TranslatableAdmin):
    pass


class RegionAdmin(TranslatableAdmin):
    pass


class WASHMapDataAdmin(admin.ModelAdmin):
    list_filter = ('country',)
    list_display = (
        'country',
        'sanitation_increase',
        'sanitation_initial',
        'sanitation_pop_current',
        'sanitation_pop_universal',
        'water_increase',
        'water_initial',
        'water_pop_current',
        'water_pop_universal')

admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(WASHMapData, WASHMapDataAdmin)
