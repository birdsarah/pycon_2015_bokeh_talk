from __future__ import unicode_literals, absolute_import
import pytest

from django.core.urlresolvers import reverse

from django_harness.translation import TranslationTestMixin

from main.models import Country
from ..models import StatGroup, StatDescription

"""
======================== FIXTURES =======================
"""


@pytest.fixture
def tt():
    ttm = TranslationTestMixin()
    ttm.counter = 0
    return ttm


@pytest.fixture
def group_a(tt):
    ttg = tt.create(StatGroup, description="Stat Group A", order=1)
    return ttg


@pytest.fixture
def stat_a_i(tt, group_a):
    ttd = tt.create(StatDescription,
                    group=group_a,
                    description="I am a statistic with (units) in Group A",
                    order=1)
    return ttd


@pytest.fixture
def stat_a_ii(tt, group_a):
    ttd = tt.create(StatDescription,
                    group=group_a,
                    description="I am a diff stat in Group A",
                    order=2)
    return ttd


@pytest.fixture
def group_b(tt):
    ttg = tt.create(StatGroup, description="Stat Group B", order=2)
    return ttg


@pytest.fixture
def stat_b_i(tt, group_b):
    ttd = tt.create(StatDescription,
                    group=group_b,
                    description="I am a statistic with (units) in Group B",
                    order=3)
    return ttd


@pytest.fixture
def zambia(tt):
    # A CMS Translated instance of Zambia
    translated_zambia = tt.create(Country, slug='zambia', local_name="Zambia")
    return translated_zambia


@pytest.fixture
def summary_url(zambia):
    return reverse('country-summary', kwargs={'country': zambia.slug})


@pytest.fixture
def comparison_url(zambia):
    return reverse('country-comparison', kwargs={'country': zambia.slug})
