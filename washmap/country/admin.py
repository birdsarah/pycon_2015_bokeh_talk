from __future__ import absolute_import, unicode_literals

from django.contrib import admin
from hvad.admin import TranslatableAdmin

from .models import (
    Country,
    Region,
)


class CountryAdmin(TranslatableAdmin):
    pass


class RegionAdmin(TranslatableAdmin):
    pass


admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
