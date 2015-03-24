# encoding: utf-8
from __future__ import unicode_literals, absolute_import

import pytest

from bs4 import BeautifulSoup
from django_dynamic_fixture import G


from main.models import Country
from ..models import StatValue


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_basic_stat_presence(
    group_a, stat_a_i, zambia, comparison_url, client
):
    G(StatValue, description=stat_a_i, country=zambia)
    response = client.get(comparison_url)
    assert response.status_code == 200
    assert group_a.description in response.content.decode('utf-8')
    assert stat_a_i.description in response.content.decode('utf-8')


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_two_groups_shown(
    stat_a_i, stat_b_i, group_a, group_b, zambia, comparison_url, client
):

    # Create stats for angola and zambia to display
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_b_i, country=zambia)

    # Get the Zambia Page
    response = client.get(comparison_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two group names displayed
    group_headings = soup.find_all(class_="_declaration_name _group_name")
    assert len(group_headings) == 2

    assert group_a.description in group_headings[0].find("th").text
    assert group_b.description in group_headings[1].find("th").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_two_groups_shown_in_set_order(
    stat_a_i, stat_b_i, group_a, group_b, zambia, comparison_url, client
):
    group_a.order = 3
    group_a.save()

    # Create stats for angola and zambia to display
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_b_i, country=zambia)

    # Get the Zambia Page
    response = client.get(comparison_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two group names displayed
    group_headings = soup.find_all(class_="_declaration_name _group_name")
    assert len(group_headings) == 2

    # First group B then group A
    assert group_b.description in group_headings[0].find("th").text
    assert group_a.description in group_headings[1].find("th").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_most_recent_year_shown_for_two_countries(
    tt, stat_a_i, zambia, comparison_url, client
):
    angola = tt.create(Country, slug='angola', local_name="Angola")

    # Create stats for angola and zambia to display
    G(StatValue, description=stat_a_i, country=zambia, year=2013, value=1)
    G(StatValue, description=stat_a_i, country=zambia, year=2014, value=2)
    G(StatValue, description=stat_a_i, country=angola, year=2011, value=3)
    G(StatValue, description=stat_a_i, country=angola, year=2010, value=4)

    # Get the Zambia Page
    response = client.get("%s?country=%s" % (comparison_url, angola.slug))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect a row with the correct description
    stats_row = soup.find_all(class_="_stat")
    assert len(stats_row) == 1
    assert stat_a_i.description in stats_row[0].find_all(class_="_description")[0].text  # nopep8

    # Expect the first column to have the zambian latest, and the second, the
    # angolan latest
    stats_cells = stats_row[0].find_all(class_="_stat_cell")
    assert len(stats_cells) == 2
    # For Zambia
    assert "2" in stats_cells[0].find(class_="_stat_value").text
    assert "2014" in stats_cells[0].find(class_="_stat_year").text
    # For Angola
    assert "3" in stats_cells[1].find(class_="_stat_value").text
    assert "2011" in stats_cells[1].find(class_="_stat_year").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_not_visible_gives_a_blank_stat_value_and_no_stat_year(
    tt, stat_a_i, zambia, comparison_url, client
):
    angola = tt.create(Country, slug='angola', local_name="Angola")

    # Create stats for angola and zambia to display
    G(StatValue, description=stat_a_i, country=zambia, year=201, visible=False)
    G(StatValue, description=stat_a_i, country=zambia, year=200, visible=False)
    G(StatValue, description=stat_a_i, country=angola, year=2010, value=4)

    # Get the Zambia Page
    response = client.get("%s?country=%s" % (comparison_url, angola.slug))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect a row with the correct description
    stats_row = soup.find_all(class_="_stat")
    assert len(stats_row) == 1

    # Expect the first column to have the zambian latest, and the second, the
    # angolan latest
    stats_cells = stats_row[0].find_all(class_="_stat_cell")
    assert len(stats_cells) == 2
    # For Zambia expect &nbsp; (in unicode form \xa0).
    assert u'\xa0' in stats_cells[0].find(class_="_stat_value").text
    assert len(stats_cells[0].find_all(class_="_stat_year")) == 0


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_not_data_and_no_stat_year_if_nothing_for_country(
    tt, stat_a_i, zambia, comparison_url, client
):
    angola = tt.create(Country, slug='angola', local_name="Angola")

    # Create stats for angola forcing zambia to show no data
    G(StatValue, description=stat_a_i, country=angola, year=2010, value=4)

    # Get the Zambia Page
    response = client.get("%s?country=%s" % (comparison_url, angola.slug))
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect a row with the correct description
    stats_row = soup.find_all(class_="_stat")
    assert len(stats_row) == 1

    # Expect the first column to have the zambian latest, and the second, the
    # angolan latest
    stats_cells = stats_row[0].find_all(class_="_stat_cell")
    assert len(stats_cells) == 2
    # For Zambia
    assert "No data" in stats_cells[0].find(class_="_stat_value").text
    assert len(stats_cells[0].find_all(class_="_stat_year")) == 0

    # Confirm Angola
    assert "4" in stats_cells[1].find(class_="_stat_value").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_not_data_with_a_year_if_no_data_explicitly_exists(
    tt, stat_a_i, zambia, comparison_url, client
):
    # Create stats for angola forcing zambia to show no data
    G(StatValue, description=stat_a_i, country=zambia, year=2010, value=None)

    # Get the Zambia Page
    response = client.get(comparison_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect a row with the correct description
    stats_row = soup.find_all(class_="_stat")
    assert len(stats_row) == 1

    stats_cells = stats_row[0].find_all(class_="_stat_cell")
    # For Zambia
    assert "No data" in stats_cells[0].find(class_="_stat_value").text
    assert "2010" in stats_cells[0].find(class_="_stat_year").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_data_is_humanized_for_long_number(
    tt, stat_a_i, zambia, comparison_url, client
):
    # Create stats for angola forcing zambia to show no data
    G(StatValue, description=stat_a_i, country=zambia, year=10, value=1000000)

    # Get the Zambia Page
    response = client.get(comparison_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect a row with the correct description
    stats_row = soup.find_all(class_="_stat")
    assert len(stats_row) == 1

    stats_cells = stats_row[0].find_all(class_="_stat_cell")
    assert "1M" in stats_cells[0].find(class_="_stat_value").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_data_is_humanized_for_small_number(
    tt, stat_a_i, zambia, comparison_url, client
):
    # Create stats for angola forcing zambia to show no data
    G(StatValue, description=stat_a_i, country=zambia, year=10, value=1.23482)

    # Get the Zambia Page
    response = client.get(comparison_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect a row with the correct description
    stats_row = soup.find_all(class_="_stat")
    assert len(stats_row) == 1

    stats_cells = stats_row[0].find_all(class_="_stat_cell")
    assert "1.23" in stats_cells[0].find(class_="_stat_value").text
