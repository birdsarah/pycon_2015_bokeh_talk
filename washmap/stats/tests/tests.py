from __future__ import unicode_literals, absolute_import

from decimal import Decimal

from StringIO import StringIO

from django.core.urlresolvers import reverse
from django.test import TestCase

from django_dynamic_fixture import G

from django_harness.fast_dispatch import FastDispatchMixin
from django_harness.dates import DateUtilsMixin
from django_harness.fast_dispatch import FastDispatchMixin
from django_harness.html_parsing import HtmlParsingMixin
from django_harness.override_settings import override_settings
from django_harness.plugin_testing import PluginTestMixin
from django_harness.translation import TranslationTestMixin
from django_harness.words import WordUtilsMixin

from main.models import Country
from ..models import StatDescription, StatValue


class StatVisibilityTests(TranslationTestMixin, TestCase):
    counter = 1

    def setUp(self):
        self.zambia = self.create(Country, name='Zambia')
        self.egypt = self.create(Country, name='Egypt')

        water = self.create(StatDescription, description="Water")
        sanitation = self.create(StatDescription, description="Sanitation")

        self.zambia_water = G(StatValue, country=self.zambia, description=water)
        self.zambia_sanitation = G(StatValue, country=self.zambia, description=sanitation)
        self.egypt_water = G(StatValue, country=self.egypt, description=water)
        self.egypt_sanitation = G(StatValue, country=self.egypt, description=sanitation)

    def test_visible_stat_manager(self):
        StatValue.objects.filter(country=self.zambia).update(visible=False)
        self.assertEqual(2, StatValue.objects.filter(visible=False).count())

        values = StatValue.visible_objects.all()

        ids = lambda x: x.id

        self.assertQuerysetEqual(
            values,
            [self.egypt_water.id, self.egypt_sanitation.id],
            transform=lambda x: x.id
        )

class StatsImportPageTests(DateUtilsMixin, FastDispatchMixin,
    HtmlParsingMixin, PluginTestMixin, TranslationTestMixin, WordUtilsMixin,
    TestCase):

    def setUp(self):
        super(StatsImportPageTests, self).setUp()

        from django.contrib.auth.models import User
        self.user = G(User, is_superuser=True, is_staff=True)

    def test_admin_homepage_links_to_country_stats_import(self):
        response = self.fast_dispatch('admin:index')
        self.assertEqual(200, response.status_code)
        response.render()

        admin_relative_url = reverse('admin:country-stats')
        assert admin_relative_url.startswith('/admin/')
        admin_relative_url = admin_relative_url[7:]
        self.assertIn(admin_relative_url, response.content)

    def test_import_root_page_loads(self):
        response = self.fast_dispatch('admin:country-stats')
        self.assertEqual(200, response.status_code)

    def test_import_root_page_loads_with_middleware(self):
        # Use self.client.get instead of fast_dispatch to ensure that
        # all middleware is hit. A problem with importing app URLs was
        # triggered by LocaleMiddleware and not reproducible with
        # fast_dispatch.
        response = self.client.get(reverse('admin:country-stats'))
        self.assertEqual(200, response.status_code)

    def test_import_root_page_contains_form(self):
        response = self.fast_dispatch('admin:country-stats')
        tree = self.parse(response)
        content = self.query(tree, '.content-wrapper')
        form = self.query(content, 'form')
        self.assertEqual(form.get('method'), 'post')
        self.assertEqual(form.get('enctype'), 'multipart/form-data')
        self.assertEqual(
            self.query(form, 'input[type="submit"]').get('name'),
            'export',
            msg="The form should contain an export button;\n%s"
                % self.tostring(form))

    def test_import_form_requires_statistic_type(self):
        response = self.fast_dispatch(
            'admin:country-stats',
            method='post',
            request_extras=dict(csrf_processing_done=True),
            post_params={
                'statistic': '',  # No statistic selected
                'export': 'Whee!'
            })
        self.assertEqual(200, response.status_code)
        form = response.context_data['form']
        # Expect form errors
        self.assertIn('statistic', form.errors)

    def test_export_button_redirects_to_export_view(self):
        statistic = G(StatDescription)
        response = self.fast_dispatch(
            'admin:country-stats',
            method='post',
            request_extras=dict(csrf_processing_done=True),
            post_params={
                'statistic': str(statistic.id),
                'export': 'Whee!'
            })
        self.assert_redirected_mini(
            response,
            reverse(
                'admin:country-stats-template',
                kwargs={'statistic': statistic.id}
                )
            )



class StatsExportTemplateTests(DateUtilsMixin, FastDispatchMixin,
    HtmlParsingMixin, PluginTestMixin, TranslationTestMixin, WordUtilsMixin,
    TestCase):

    counter = 1

    def setUp(self):
        super(StatsExportTemplateTests, self).setUp()

        from django.contrib.auth.models import User
        self.user = G(User, is_superuser=True, is_staff=True)

        self.water = self.create(StatDescription, description="Water", code="water")

    def test_import_root_page_loads_properly_directly(self):
        response = self.fast_dispatch('admin:country-stats')
        self.assertEqual(200, response.status_code)

    def test_import_root_page_loads_properly_with_middleware(self):
        # Use self.client.get instead of fast_dispatch to ensure that
        # all middleware is hit. A problem with importing app URLs was
        # triggered by LocaleMiddleware and not reproducible with
        # fast_dispatch.
        response = self.client.get(reverse('admin:country-stats'))
        self.assertEqual(200, response.status_code)

    def assert_export_template(self, statistic=None):
        if statistic is None:
            statistic = StatDescription.objects.get()

        response = self.fast_dispatch('admin:country-stats-template',
            url_kwargs={'statistic': statistic.id})
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            response['Content-Disposition'],
            'attachment; filename=%s' % ('country-stats-%s.csv' % statistic.code))

        import tablib
        from tablib.formats import _csv
        data = tablib.Dataset()
        _csv.import_set(data, response.content)
        return data

    def test_export_has_ordered_country_column(self):
        countries = ['B', 'C', 'A']
        for country in countries:
            self.create(Country, name=country)
        data = self.assert_export_template()

        actual_rows = [d['country'] for d in data.dict]
        self.assertEqual(actual_rows, ['A', 'B', 'C'])

    def test_exports_have_ordered_year_columns(self):
        zambia = self.create(Country, 'Zambia')

        # Expect year columns to be displayed ordered by year
        G(StatValue, description=self.water, country=zambia, year=2014)
        G(StatValue, description=self.water, country=zambia, year=2012)

        # Add a year which we do not expect to see in the export for 'water' as
        # it belongs to another data set (ie. 'santiation').
        sanitation = self.create(StatDescription, description="Sanitation")
        G(StatValue, description=sanitation, country=zambia, year=2013)

        # Test export for 'Water' data (in year order)
        data = self.assert_export_template(statistic=self.water)
        self.assertEqual(data.headers[1:], ['2012', '2014'])

        # Text export for 'Sanitation' data
        data = self.assert_export_template(statistic=sanitation)
        self.assertEqual(data.headers[1:], ['2013'])

    def test_export_contains_values(self):
        zambia = self.create(Country, name='Zambia')

        G(StatValue, description=self.water, country=zambia, year=2012, value=200.00000)
        G(StatValue, description=self.water, country=zambia, year=2013, value=300.00001)

        data = self.assert_export_template(statistic=self.water)

        self.assertEqual(1, len(data.dict))
        zambia_row = data.dict[0]
        self.assertEqual('Zambia', zambia_row['country'])

        # For readability we expect trailing zeros to be removed.
        self.assertEqual(zambia_row['2012'], '200')
        self.assertEqual(zambia_row['2013'], '300.00001')


    def test_export_can_contain_missing_values(self):
        zambia = self.create(Country, name='Zambia')
        algeria = self.create(Country, name='Algeria')

        G(StatValue, description=self.water, country=zambia, year=2012, value=300.00001)

        data = self.assert_export_template(statistic=self.water)

        self.assertEqual(2, len(data.dict))
        algeria_row = data.dict[0]
        self.assertEqual('Algeria', algeria_row['country'])
        self.assertEqual(algeria_row['2012'], '')

    def test_import_template(self):
        country = self.create(Country, name='Zambia')
        statistic = G(StatDescription)

        # Export template
        data = self.assert_export_template(statistic=statistic)

        # Add new column for 2012
        data.append_col(lambda _: '111.11', header='2012')

        csv_file = StringIO(data.csv)
        csv_file.name = "statistic.csv"

        response = self.fast_dispatch('admin:country-stats',
            method='post',
            post_params={
                'statistic': str(statistic.id),
                'upload': csv_file,
            },
            request_extras=dict(csrf_processing_done=True)
        )

        self.assert_redirected_mini(response, reverse('admin:country-stats'))

        value = StatValue.objects.get(
            year=2012,
            country=country,
            description=statistic
        )
        self.assertEqual(value.value, Decimal('111.11'))
