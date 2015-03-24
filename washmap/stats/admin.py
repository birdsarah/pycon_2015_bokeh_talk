from __future__ import absolute_import, unicode_literals

from django.contrib import admin


from .models import (
    StatDescription,
    StatValue
)


class StatValueAdmin(admin.ModelAdmin):
    list_display = ('description', 'year', 'country', 'value')
    list_filter = ('description', 'country', 'year')


admin.site.register(StatDescription)
admin.site.register(StatValue, StatValueAdmin)
