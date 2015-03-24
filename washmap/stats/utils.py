from __future__ import absolute_import, unicode_literals
from django.utils import simplejson

from collections import Counter

from django.db.models import Max, Min

from .models import StatValue, StatDescription, StatGroup


def get_stats_groups_descriptions(countries, visible=None):
    stats = StatValue.objects.filter(country__in=countries)
    if visible:
        stats = stats.filter(visible=visible)  # nopep8

    stats_groups = StatGroup.objects.filter(
        statdescription__statvalue__in=stats
    ).distinct().order_by('order')

    stats_descriptions = StatDescription.objects.filter(
        statvalue__in=stats
    ).distinct().order_by('order')
    return (stats_groups, stats_descriptions, stats)


def get_latest_stats_for_multiple_countries(countries, visible=None):
    """
    Produce a dictionary of stat values given:
        * countries - the list of countries required
        * and visible flag
    """
    stats_groups, stats_descriptions, stats = \
        get_stats_groups_descriptions(countries, visible)

    stat_dictionary = {}
    for c in countries:
        stat_dictionary[c] = {}
        for d in stats_descriptions:
            try:
                stat_value = StatValue.objects.filter(
                    country=c, description=d
                ).latest('year')
            except StatValue.DoesNotExist:
                stat_value = None
            stat_dictionary[c][d] = stat_value
    return (stats_groups, stats_descriptions, stat_dictionary)


def show_graph(d, stats_for_graph):
    """
    We hide the graph if:
        * On the admin the user has chosen to hide the graph
        * There is only one value (there could be multiple Nones as well)
    """
    show_graph = True
    if d.hide_graph:
        show_graph = False
    if len(stats_for_graph) < 2:
        show_graph = False
    return show_graph


def _build_stat_dictionary(stats_descriptions, stats):
    stat_dictionary = {}
    for d in stats_descriptions:
        minmax = StatValue.objects.filter(
            description=d).aggregate(min=Min('value'), max=Max('value'))
        stats_list = stats.filter(description=d).order_by('-year')
        stats_for_graph = stats_list.exclude(value=None).values('value',
                                                                'year')
        hide_graph = not show_graph(d, stats_for_graph)
        json_stats_list = simplejson.dumps(list(stats_for_graph))
        stat_dictionary[d] = {}
        stat_dictionary[d]["stats_values"] = stats_list
        stat_dictionary[d]["statsValuesJSON"] = json_stats_list
        stat_dictionary[d]["minY"] = minmax['min']
        stat_dictionary[d]["maxY"] = minmax['max']
        stat_dictionary[d]["hideGraph"] = hide_graph
    return stat_dictionary


def get_all_stats_for_one_country(country, visible=None):
    """
    Produce a dictionary of stat values given:
        * countries - the list of countries required
        * and visible flag
    """
    stats_groups, stats_descriptions, stats = \
        get_stats_groups_descriptions([country], visible)

    stat_dictionary = _build_stat_dictionary(stats_descriptions, stats)

    return (stats_groups, stats_descriptions, stat_dictionary)


def get_all_stats_for_one_country_one_group(country, group, visible=None):
    """
    Produce a dictionary of stat values given:
        * countries - the list of countries required
        * and visible flag
    """
    stats = StatValue.objects.filter(country=country)
    stats = stats.filter(description__group=group)
    if visible:
        stats = stats.filter(visible=visible)

    stats_descriptions = StatDescription.objects.filter(
        statvalue__in=stats
    ).distinct().order_by('order')

    stat_dictionary = _build_stat_dictionary(stats_descriptions, stats)

    return stats_descriptions, stat_dictionary
