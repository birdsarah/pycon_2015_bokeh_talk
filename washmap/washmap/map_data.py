from __future__ import unicode_literals, absolute_import

from bokeh.models import ColumnDataSource
from pandas import DataFrame, merge
from numpy import where

from country.models import Country
from main.utils import build_coords_lists
from stats.models import StatValue

from .chart_constants import SANITATION_COLOR_RANGE, WATER_COLOR_RANGE, GRAY


def update_active_data(data, active_year, palette_name=None):
    # Default to water
    palette = WATER_COLOR_RANGE
    if palette_name == 'sanitation':
        palette = SANITATION_COLOR_RANGE

    def _get_color(value):
        if value < 0:
            return GRAY
        index = int(value / 10)
        return palette[index]

    data['active_year'] = active_year
    data['active_year_value'] = data[active_year]
    data['color_for_active_year'] = data[active_year].apply(_get_color)
    data['active_year_value'] = where(data['active_year_value'] < 0, '-', data['active_year_value'])  # nopep8
    return data


def get_frame_for_country(frame, country):
    return frame[frame.name == country]


def get_data_with_countries(year_of_color=1990, stat_code='WNTI_%', palette=None):  # nopep8
    if not palette:
        palette = WATER_COLOR_RANGE

    # Get the countries data frame
    countries = Country.objects.exclude(boundary='')
    countries = countries.filter(region__in=[1, 2, 3, 6, 7])  # Africa only
    countries = countries.values('name', 'boundary', 'id')
    countries_df = DataFrame.from_records(countries)
    countries_df['xs'], countries_df['ys'] = build_coords_lists(countries_df['boundary'])  # nopep8

    # Get the stats for access to water
    stats = StatValue.objects.filter(description__code=stat_code)
    stats = stats.values('value', 'year', 'country_id')
    stats_df = DataFrame.from_records(stats, coerce_float=True)

    data_as_dict = DataFrame(
        stats_df.groupby('country_id').apply(
            lambda x: ColumnDataSource({'watsan': x.value, 'year': x.year})
        ),
        columns=['line_source']
    )
    # Pivot it before merging
    pivot_df = stats_df.pivot(columns='year', index='country_id', values='value')  # nopep8
    pivot_df = pivot_df.join(data_as_dict)
    pivot_df['id'] = pivot_df.index

    # Merge the countries and stats together
    merged_df = merge(countries_df, pivot_df, how='left')
    merged_df = merged_df.fillna(value=-99)

    # Color it
    colored_df = update_active_data(merged_df, year_of_color, palette)

    # Otherwise things are sad!
    colored_df.columns = colored_df.columns.astype('str')
    return colored_df


def get_water_data_with_countries(year=1990):
    return get_data_with_countries(year, 'WNTI_%', 'water')


def get_sanitation_data_with_countries(year=1990):
    return get_data_with_countries(year, 'SNTI_%', 'sanitation')
