from __future__ import unicode_literals, absolute_import

from pandas import DataFrame
from numpy import where

from country.models import Country
from main.utils import build_coords_lists
from stats.models import StatValue

from .chart_constants import SANITATION_COLOR_RANGE, WATER_COLOR_RANGE, GRAY


def color_data(data):
    def _get_color(value, palette):
        if value < 0:
            return GRAY
        index = int((value-0.01) / 10)
        return palette[index]

    data['wat_color'] = data['wat_value'].apply(
        _get_color, args=([WATER_COLOR_RANGE])
    )
    data['san_color'] = data['san_value'].apply(
        _get_color, args=([SANITATION_COLOR_RANGE])
    )
    data['wat_value'] = where(data['wat_value'] < 0, '-', data['wat_value'])
    data['san_value'] = where(data['san_value'] < 0, '-', data['san_value'])
    return data


def get_countries():
    # Get the countries data frame
    countries = Country.objects.exclude(boundary='')
    countries = countries.filter(region__in=[1, 2, 3, 6, 7])  # Africa only
    countries = countries.values('name', 'boundary', 'id')
    countries_df = DataFrame.from_records(countries)
    countries_df['xs'], countries_df['ys'] = build_coords_lists(countries_df['boundary'])  # nopep8
    countries_df = countries_df.drop(['id', 'boundary'], axis=1)
    return countries_df


def get_stats_from_model(stat_code, column_name):
    # Get the stats for access to water
    stats = StatValue.objects.filter(description__code=stat_code)
    stats = stats.values('value', 'country__name', 'year')
    stats_df = DataFrame.from_records(stats, coerce_float=True)
    stats_df.rename(
        columns={
            'country__name': 'name',
            'value': column_name,
        },
        inplace=True
    )
    return stats_df


def get_wat_stats_all_years():
    wat_stats_df = get_stats_from_model('WNTI_%', 'wat_value')
    return wat_stats_df


def get_san_stats_all_years():
    san_stats_df = get_stats_from_model('SNTI_%', 'san_value')
    return san_stats_df


def get_data_with_countries(wat_stats_df, san_stats_df, year=1990):
    countries_df = get_countries()

    # Get data for year, Merge water & sanitation
    wat_stats_df = wat_stats_df[wat_stats_df.year == year]
    san_stats_df = san_stats_df[san_stats_df.year == year]
    wat_san_df = wat_stats_df.merge(san_stats_df)

    # Merge the countries and stats together
    merged_df = countries_df.merge(wat_san_df, how='left')
    merged_df = merged_df.fillna(value=-99)

    # Color it
    colored_df = color_data(merged_df)
    colored_df['year'] = year

    # Otherwise things are sad!
    colored_df.columns = colored_df.columns.astype('str')
    return colored_df


def get_line_stats_from_model(stat_code, country_name, column_name):
    # Get the stats for access to water
    stats = StatValue.objects.filter(description__code=stat_code)
    stats = stats.filter(country__name=country_name)
    stats_values = stats.values('value', 'year')
    stats_df = DataFrame.from_records(stats_values, coerce_float=True)
    stats_df.rename(columns={ 'value': column_name, }, inplace=True)
    return stats_df


def get_line_data(country_name):
    wat_stats = get_line_stats_from_model('WNTI_%', country_name, 'wat_value')
    san_stats = get_line_stats_from_model('SNTI_%', country_name, 'san_value')
    wat_san = wat_stats.merge(san_stats, on='year')
    return wat_san
