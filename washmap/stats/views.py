from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse

from custom_importer.forms import ImportFormBase
from custom_importer.views import ImporterBase, ExportTemplateBase

from country.models import Country

from .models import StatDescription, StatValue
from .statsimporter import StatisticResource


class CountryStatsForm(ImportFormBase):
    def get_choice_field_name(self):
        return 'statistic'

    def get_choice_field_queryset(self):
        return StatDescription.objects.all()


class ImportCountryStats(ImporterBase):
    form_class = CountryStatsForm

    def get_success_url(self):
        return reverse('admin:country-stats')

    def get_export_url(self, statistic):
        return reverse('admin:country-stats-template',
                       kwargs={'statistic': statistic.id})

    def get_import_resource_class(self):
        return StatisticResource


class ExportCountryStats(ExportTemplateBase):
    model = StatDescription

    def get_export_resource_class(self):
        return StatisticResource

    def get_export_set(self, kwargs):
        return StatDescription.objects.get(id=kwargs['statistic'])

    def get_export_filename(self, file_format):
        statistic = self.get_export_set(self.kwargs)
        filename = "country-stats-%s.%s" % (
            statistic.code,
            file_format.get_extension())
        return filename
