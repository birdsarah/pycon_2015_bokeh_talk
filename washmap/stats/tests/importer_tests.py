from __future__ import unicode_literals, absolute_import

import pytest

from django_dynamic_fixture import G

from decimal import Decimal

from StringIO import StringIO

from django.test import TestCase
from django.utils.datastructures import SortedDict

from ..statsimporter  import (
        StatisticResource,
        StatValueInstanceLoader,
        StatValueRowInstance,
        YearField,
        CountryField
    )

from django_harness.translation import TranslationTestMixin

from main.models import Country
from ..models import StatDescription, StatValue

@pytest.fixture
def translationtest():
    ttm = TranslationTestMixin()
    ttm.counter = 0
    return ttm

@pytest.mark.django_db
def test_na_yearfield_clean_is_null_value(translationtest):
    data = SortedDict([('2015', 'NA')])
    field = YearField(2015, column_name="%s" % 2015)
    assert None == field.clean(data)

@pytest.mark.django_db
def test_import_dataset(translationtest):
    statistic = translationtest.create(StatDescription)
    country = translationtest.create(Country, name='Zambia')
    resource = StatisticResource(statistic)

    import tablib
    data = tablib.Dataset()
    data.headers = ('country', '2013', '2014', '2015', '2016')
    data.append(('Zambia', '11.11', '22.22', '', 'NA'))

    result = resource.import_data(data, raise_errors=False)

    for i, row in enumerate(result.rows):
        for n, error in enumerate(row.errors):
            pytest.fail("row %i, error %i: %s\n traceback: %s" % (
                        i, n, error.error, error.traceback))

    values = StatValue.objects.filter(description=statistic, country=country)
    actual = dict(values.values_list('year', 'value'))
    expected = {2013: Decimal('11.11'), 2014: Decimal('22.22'), 2016: None}

    assert actual == expected

@pytest.mark.django_db
def test_export_dataset(translationtest):
    statistic = translationtest.create(StatDescription)
    country = translationtest.create(Country, name='Zambia')
    G(StatValue, description=statistic, country=country, year=2011, value='11.11')
    G(StatValue, description=statistic, country=country, year=2012, value=None)

    resource = StatisticResource(statistic)
    data = resource.export()
    expected = [{'country': 'Zambia', '2011': '11.11', '2012': 'NA'}]
    assert data.dict == expected

@pytest.mark.django_db
def test_export_yearfield_returns_rendered_stat_value(translationtest):
    statistic = translationtest.create(StatDescription)
    country = translationtest.create(Country, name='Zambia')
    G(StatValue, description=statistic, country=country, year=2011,
      value='11.11')
    stat = StatValueRowInstance(statistic=statistic, country=country)

    # A YearField represents a column for a year (rows are countries and cells
    # stat values).

    year = 2011
    field = YearField(year, column_name='%s' % year)

    # The export method should return a stat value (if it exists) for the
    # current row.
    assert '11.11' == field.export(stat)


@pytest.mark.django_db
def test_get_queryset_returns_statvalue_instances(translationtest):
    statistic = translationtest.create(StatDescription)
    country = translationtest.create(Country, name='Zambia')
    G(StatValue, description=statistic, country=country, year=2011,
      value='11.11')

    resource = StatisticResource(statistic)
    statvalues = resource.get_queryset()

    # Get the existing statvalues: calling iterator() is an ugly hack to deal
    # with import-export's assumption it gets given a queryset.
    values = statvalues.iterator()
    assert len(values) == 1
    assert values[0].country == country
    assert values[0].statistic == statistic


@pytest.mark.django_db
def test_export_statistic_resource(translationtest):
    statistic = translationtest.create(StatDescription)
    country = translationtest.create(Country, name='Zambia')
    G(StatValue, description=statistic, country=country, year=2011,
      value='11.11')

    stat = StatValueRowInstance(statistic=statistic, country=country)
    resource = StatisticResource(statistic)
    assert ['Zambia', '11.11'] == resource.export_resource(stat)
