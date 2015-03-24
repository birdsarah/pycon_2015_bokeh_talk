from __future__ import unicode_literals, absolute_import

import json
import pytest

from bs4 import BeautifulSoup
from django_dynamic_fixture import G

from django.contrib.auth.models import User
from django.utils import translation

from main.models import Country
from country_comparison.views import CountrySummary
from ..models import StatValue


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_basic_stat_presence(
    group_a, stat_a_i, zambia, summary_url, client
):
    G(StatValue, description=stat_a_i, country=zambia)
    response = client.get(summary_url)
    assert response.status_code == 200
    assert group_a.description in response.content.decode('utf-8')
    assert stat_a_i.description in response.content.decode('utf-8')


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_two_groups_shown(
    group_a, stat_a_i, group_b, stat_b_i, zambia, summary_url, client
):

    # Create a stat in group A & group B for Zambia
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_b_i, country=zambia)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two blocks, one for each group
    stats_blocks = soup.find_all(class_="_stats")
    assert len(stats_blocks) == 2

    stat_block_a = stats_blocks[0]
    stat_block_b = stats_blocks[1]
    assert stat_block_a.find(class_="_stats-group-heading").text == \
        group_a.description
    assert stat_block_b.find(class_="_stats-group-heading").text == \
        group_b.description


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_one_group_shown_if_stat_not_for_country(
    tt, group_a, stat_a_i, stat_b_i, zambia, summary_url, client
):
    angola = tt.create(Country, slug='angola', local_name="Angola")

    # Create a stat in group A for Zambia, and group B for Angola
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_b_i, country=angola)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect only a block for group A
    stats_blocks = soup.find_all(class_="_stats")
    assert len(stats_blocks) == 1
    assert stats_blocks[0].find(class_="_stats-group-heading").text == \
        group_a.description


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_display_respects_group_order(
    group_a, stat_a_i, group_b, stat_b_i, zambia, summary_url, client
):
    group_a.order = 3
    group_a.save()

    # Create a stat in group A & group B for Zambia
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_b_i, country=zambia)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two blocks, one for each group, with the order B then A
    stats_blocks = soup.find_all(class_="_stats")
    assert len(stats_blocks) == 2

    stat_block_a = stats_blocks[1]  # Note a should be second
    stat_block_b = stats_blocks[0]
    assert stat_block_a.find(class_="_stats-group-heading").text == \
        group_a.description
    assert stat_block_b.find(class_="_stats-group-heading").text == \
        group_b.description


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_stat_descriptions_respect_group_order(
    group_a, stat_a_i, stat_a_ii, zambia, summary_url, client
):

    # Create a stat in a_i & a_ii for Zambia
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_a_ii, country=zambia)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two rows of stats in order stat_a_i, stat_a_ii
    stats_rows = soup.find_all(class_="panel-stats")
    stat_row_a_i = stats_rows[0]
    stat_row_a_ii = stats_rows[1]

    assert stat_a_i.description in stat_row_a_i.find(class_="title").text
    assert stat_a_ii.description in stat_row_a_ii.find(class_="title").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_stat_descriptions_respect_group_order_when_changed(
    group_a, stat_a_i, stat_a_ii, zambia, summary_url, client
):

    # Create a stat in a_i & a_ii for Zambia
    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_a_ii, country=zambia)

    # Change stat order
    stat_a_i.order = 3
    stat_a_i.save()

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two rows of stats in NEW order stat_a_ii, stat_a_i
    stats_rows = soup.find_all(class_="panel-stats")
    assert len(stats_rows) == 2
    stat_row_a_ii = stats_rows[0]
    stat_row_a_i = stats_rows[1]

    assert stat_a_i.description in stat_row_a_i.find(class_="title").text
    assert stat_a_ii.description in stat_row_a_ii.find(class_="title").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_stat_narrative_appears(
    stat_a_i, zambia, summary_url, client
):

    G(StatValue, description=stat_a_i, country=zambia)

    # Add narrative to stat
    stat_a_i.narrative = "Oh! To be a mighty, mighty developer."
    stat_a_i.save()

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two rows of stats in NEW order stat_a_ii, stat_a_i
    narratives = soup.find_all(class_="narrative")
    assert len(narratives) == 1
    assert "Oh! To be a mighty, mighty developer." in narratives[0].text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_stat_narrative_appears_in_french(
    stat_a_i, zambia, summary_url, rf
):
    G(StatValue, description=stat_a_i, country=zambia)

    # Add a translated narrative
    stat_a_i.translate('fr')
    stat_a_i.narrative = "Mais oui!"
    stat_a_i.save()

    # Get the French Zambia Page
    translation.activate('fr')
    request = rf.get(summary_url)
    request.user = G(User)
    request.LANGUAGE_CODE = 'en'
    view = CountrySummary.as_view()
    response = view(request, country=zambia)
    response.render()
    assert response.status_code == 200

    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect two rows of stats in NEW order stat_a_ii, stat_a_i
    narratives = soup.find_all(class_="narrative")
    assert len(narratives) == 1
    assert "Mais oui!" in narratives[0].text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_table_in_detail_with_one_row(
    stat_a_i, zambia, summary_url, client
):

    G(StatValue, description=stat_a_i, country=zambia, year=2010, value=1)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect table in summary
    data_views = soup.find_all(class_="data-view")
    assert len(data_views) == 1
    table = data_views[0].table

    # With two rows
    rows = table.find_all("tr")
    assert len(rows) == 2

    # With first row having headers
    assert rows[0].find_all("th")[0].text == 'Year'
    assert rows[0].find_all("th")[1].text == 'Value'

    # And second row having stat_value
    assert "2010" in rows[1].find_all("td")[0].text
    assert "1" in rows[1].find_all("td")[1].find_all(class_="_stat_value")[0].text  # nopep8


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_table_with_multiple_rows(
    stat_a_i, zambia, summary_url, client
):

    G(StatValue, description=stat_a_i, country=zambia, year=2010, value=1)
    G(StatValue, description=stat_a_i, country=zambia, year=2011, value=2)
    G(StatValue, description=stat_a_i, country=zambia, year=2012, value=3)

    stat_a_i.hide_graph = True
    stat_a_i.save()

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect table in summary
    data_views = soup.find_all(class_="data-view")
    assert len(data_views) == 1
    table = data_views[0].table

    # With four rows (one for header, one for each stat)
    rows = table.find_all("tr")
    assert len(rows) == 4


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_stat_row_displays_latest_stat_in_title(
    stat_a_i, zambia, summary_url, client
):

    G(StatValue, description=stat_a_i, country=zambia, year=2010, value=1)
    G(StatValue, description=stat_a_i, country=zambia, year=2011, value=2)
    G(StatValue, description=stat_a_i, country=zambia, year=2012, value=3)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect
    stats_rows = soup.find_all(class_="summary")
    assert len(stats_rows) == 1

    assert "2012" in stats_rows[0].find(class_="title").text
    assert "3" in stats_rows[0].find(class_="value").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_id_and_data_attr_are_correct(
    stat_a_i, zambia, summary_url, client
):
    """
    For javascript to work correctly, the id in needs to be set on the detail
    div, and the data-attr on the summary div.
    """

    G(StatValue, description=stat_a_i, country=zambia)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect
    stats_row = soup.find(class_="panel-stats")
    summary = stats_row.find(class_="summary")
    detail = stats_row.find(class_="detail")

    assert summary.attrs["data-target"] == "#collapse_%s" % (stat_a_i.pk)
    assert detail.attrs["id"] == "collapse_%s" % (stat_a_i.pk)


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_if_stat_not_visible_not_in_table(
    stat_a_i, stat_a_ii, zambia, summary_url, client
):
    """
    For javascript to work correctly, the id in needs to be set on the detail
    div, and the data-attr on the summary div.
    """

    G(StatValue, description=stat_a_i, country=zambia)
    G(StatValue, description=stat_a_ii, country=zambia, visible=False)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect one row of stats only
    stats_rows = soup.find_all(class_="panel-stats")
    assert len(stats_rows) == 1
    stat_row_a_i = stats_rows[0]

    assert stat_a_i.description in stat_row_a_i.find(class_="title").text


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_if_stat_value_is_null_then_displays_no_data(
    stat_a_i, zambia, summary_url, client
):

    G(StatValue, description=stat_a_i, country=zambia, year=2010, value=None)

    # Get the Zambia Page
    response = client.get(summary_url)
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect table in summary
    data_views = soup.find_all(class_="data-view")
    assert len(data_views) == 1
    table = data_views[0].table
    rows = table.find_all("tr")

    # And row of table reads No Data
    assert "No data" in rows[1].find_all("td")[1].find_all(class_="_stat_value")[0].text  # nopep8


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_graph_view_class_not_present_when_only_one_statvalue(
    client, stat_a_i, zambia, summary_url
):
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect no show-sparkline and no graph-view
    graphview = soup.find_all(class_="graph-view")
    assert len(graphview) == 0


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_graph_view_class_not_present_when_no_datas_and_one_statvalue(
    client, stat_a_i, zambia, summary_url
):
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)
    G(StatValue, description=stat_a_i, country=zambia, value=None, year=10)
    G(StatValue, description=stat_a_i, country=zambia, value=None, year=11)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect no show-sparkline and no graph-view
    graphview = soup.find_all(class_="graph-view")
    assert len(graphview) == 0


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_graph_view_class_present_when_two_statvalues_and_one_none(
    client, stat_a_i, zambia, summary_url
):
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)
    G(StatValue, description=stat_a_i, country=zambia, value=2.4, year=10)
    G(StatValue, description=stat_a_i, country=zambia, value=None, year=14)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect graph-view
    graphview = soup.find_all(class_="graph-view")
    assert len(graphview) == 1


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_show_sparkling_class_not_present_when_only_one_statvalue(
    client, stat_a_i, zambia, summary_url
):
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect no show-sparkline and no graph-view
    sparkline = soup.find_all(class_="show-sparkline")
    assert len(sparkline) == 0


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_graph_view_class_not_present_when_stat_marked_to_hide(
    client, stat_a_i, zambia, summary_url
):
    stat_a_i.hide_graph = True
    stat_a_i.save()

    # You need two stat values to make a chart
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)
    G(StatValue, description=stat_a_i, country=zambia, value=2.33, year=11)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect no show-sparkline and no graph-view
    graphview = soup.find_all(class_="graph-view")
    assert len(graphview) == 0


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_data_needed_for_d3_is_valid(
    stat_a_i, zambia, summary_url, client
):
    # The template localization will turn a value of 1.23 to 1,23.
    # This is awesome, except JSON can't parse it.
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect one data_div with the correctly formatted data.
    data_div = soup.find_all(class_="data")
    assert len(data_div) == 1
    data = data_div[0].get("data")
    try:
        json.loads(data)
    except ValueError:
        pytest.fail("JSON in data_div in French page is not valid")


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_if_statvalue_is_null_then_data_needed_for_d3_is_valid(
    stat_a_i, zambia, summary_url, client
):
    # The template localization will turn a value of 1.23 to 1,23.
    # This is awesome, except JSON can't parse it.
    G(StatValue, description=stat_a_i, country=zambia, year=2010, value=None)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Expect one data_div with the correctly formatted data.
    data_div = soup.find_all(class_="data")
    assert len(data_div) == 1
    data = data_div[0].get("data")
    try:
        json.loads(data)
    except ValueError:
        pytest.fail("JSON is not valid with null value")


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_data_needed_for_d3_is_not_using_localized_decimals(
    stat_a_i, zambia, summary_url, rf
):
    # The template localization will turn a value of 1.23 to 1,23.
    # This is awesome, except JSON can't parse it.
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=2010)

    # Get the French Zambia Page
    translation.activate('fr')
    request = rf.get(summary_url)
    request.user = G(User)
    request.LANGUAGE_CODE = 'en'
    view = CountrySummary.as_view()
    response = view(request, country=zambia)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Find the data div for our stat value
    data_div = soup.find_all(class_="data")
    assert len(data_div) == 1

    # Expect data in data_div can be loaded by json.loads
    data = data_div[0].get("data")
    try:
        json.loads(data)
    except ValueError:
        pytest.fail("JSON in data_div in French page is not valid")

    # Expect minY and maxY to also be in decimal format
    print data_div[0]
    miny = data_div[0].get("data-miny")
    maxy = data_div[0].get("data-maxy")
    assert "1.23" in miny
    assert "1.23" in maxy

    translation.deactivate()


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_if_value_is_none_there_is_not_row_in_data_table(
    client, stat_a_i, zambia, summary_url
):
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=12)
    G(StatValue, description=stat_a_i, country=zambia, value=2.4, year=10)
    G(StatValue, description=stat_a_i, country=zambia, value=None, year=14)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Find the data div for our stat value
    data_div = soup.find_all(class_="data")
    assert len(data_div) == 1

    # Expect data in data_div can be loaded by json.loads
    data = data_div[0].get("data")
    try:
        data_dict = json.loads(data)
    except ValueError:
        pytest.fail("JSON not valid")

    assert len(data_dict) == 2


@pytest.mark.django_db
@pytest.mark.urls('country_comparison.test_urls')
def test_if_value_is_none_there_is_valid_json(
    client, stat_a_i, zambia, summary_url
):
    G(StatValue, description=stat_a_i, country=zambia, value=None, year=10)
    G(StatValue, description=stat_a_i, country=zambia, value=1.23, year=11)
    G(StatValue, description=stat_a_i, country=zambia, value=2.4, year=12)

    response = client.get(summary_url)
    response.render()
    assert response.status_code == 200
    soup = BeautifulSoup(response.content.decode('utf-8'))

    # Find the data div for our stat value
    data_div = soup.find_all(class_="data")
    assert len(data_div) == 1

    # Expect data in data_div can be loaded by json.loads
    data = data_div[0].get("data")
    try:
        data_dict = json.loads(data)
    except ValueError:
        pytest.fail("JSON not valid")
