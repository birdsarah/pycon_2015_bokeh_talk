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


def get_frame_for_country(frame, country):
    return frame[frame.name == country]


def get_data_with_countries(year_of_color=1990):

    # Get the countries data frame
    countries = Country.objects.exclude(boundary='')
    countries = countries.filter(region__in=[1, 2, 3, 6, 7])  # Africa only
    countries = countries.values('name', 'boundary', 'id')
    countries_df = DataFrame.from_records(countries)
    countries_df['xs'], countries_df['ys'] = build_coords_lists(countries_df['boundary'])  # nopep8
    countries_df['country_id'] = countries_df['id']
    countries_df = countries_df.drop(['id', 'boundary'], axis=1)

    # Get the stats for access to water
    wat_stats = StatValue.objects.filter(description__code='WNTI_%')
    wat_stats = wat_stats.filter(year=year_of_color)
    wat_stats = wat_stats.values('value', 'country_id')
    wat_stats_df = DataFrame.from_records(wat_stats, coerce_float=True)
    wat_stats_df['wat_value'] = wat_stats_df['value']
    wat_stats_df = wat_stats_df.drop('value', axis=1)

    # Get the stats for access to sanitation
    san_stats = StatValue.objects.filter(description__code='SNTI_%')
    san_stats = san_stats.filter(year=year_of_color)
    san_stats = san_stats.values('value', 'country_id')
    san_stats_df = DataFrame.from_records(san_stats, coerce_float=True)
    san_stats_df['san_value'] = san_stats_df['value']
    san_stats_df = san_stats_df.drop('value', axis=1)

    # Merge water & sanitation
    wat_san_df = wat_stats_df.merge(san_stats_df)

    # Merge the countries and stats together
    merged_df = countries_df.merge(wat_san_df, how='left')
    merged_df = merged_df.fillna(value=-99)

    # Color it
    colored_df = color_data(merged_df)

    # Otherwise things are sad!
    colored_df['year'] = year_of_color
    colored_df.columns = colored_df.columns.astype('str')
    return colored_df


def get_water_data_for_one_country(year=1990, country="South Africa"):
    data = get_data_with_countries(year, 'WNTI_%', 'water')
    return data[data.name == 'South Africa']
