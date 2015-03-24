from __future__ import unicode_literals, absolute_import
from bokeh.models import (
    ColumnDataSource,
    Range1d,
    Plot,
    Patches,
    HoverTool,
)
from bokeh.palettes import brewer
from pandas import DataFrame, merge

from country.models import Country
from main.utils import build_coords_lists
from stats.models import StatValue
from .chart_constants import GRAY, PLOT_FORMATS


class WaterAccessMap(object):
    def get_countries(self):
        countries = Country.objects.exclude(boundary='')
        countries = countries.filter(region__in=[1, 2, 3, 6, 7])
        countries = countries.values('name', 'boundary', 'id')
        countries_df = DataFrame.from_records(countries)
        countries_df['xs'], countries_df['ys'] = build_coords_lists(countries_df['boundary'])  # nopep8
        countries_df.to_pickle('/home/bird/Dev/birdsarah/pycon_2015_bokeh_talk/presentation/pickles/countries.pickle')  # nopep8
        return countries_df

    def get_data(self):
        countries = self.get_countries()
        stats = StatValue.objects.filter(description__code='WNTI_%')
        stats = stats.values('value', 'year', 'country_id')
        stats_df = DataFrame.from_records(stats, coerce_float=True)
        pivot = stats_df.pivot(columns='year', index='country_id', values='value')  # nopep8
        pivot['id'] = pivot.index
        merged = merge(countries, pivot, how='left')
        merged = merged.fillna(value=-99)
        colored_data = self.colorize(merged)
        colored_data.to_pickle('/home/bird/Dev/birdsarah/pycon_2015_bokeh_talk/presentation/pickles/water_data.pickle')  # nopep8
        return merged

    def colorize(self, data):
        palette = brewer['Blues'][9][::-1]
        palette.append(palette[8])  # Add an extra blue on the end

        def _get_color(value):
            if value < 0:
                return GRAY
            index = int(value / 10)
            return palette[index]

        years = xrange(1990, 2013)
        for year in years:
            col_name = str(year) + '_color'
            data[col_name] = data[year].apply(_get_color)

        return data

    def construct_static(self):
        data = self.get_data()
        source = ColumnDataSource(data)

        # Plot and axes
        x_start, x_end = (-20, 60)
        y_start, y_end = (-40, 40)
        xdr = Range1d(x_start, x_end)
        ydr = Range1d(y_start, y_end)

        aspect_ratio = (x_end - x_start) / (y_end - y_start)
        plot_height = 400
        plot_width = int(plot_height * aspect_ratio)
        tooltips = [("country", "@name"),
                    ("1990", "@1990"),
                    ("2012", "@2012")]
        plot = Plot(
            x_range=xdr,
            y_range=ydr,
            title="",
            plot_width=plot_width,
            plot_height=plot_height,
            background_fill="#FAFAFA",
            **PLOT_FORMATS
        )

        borders = Patches(
            xs='xs', ys='ys',
            fill_color='1990_color', fill_alpha=1,
            line_color='1990_color', line_width=0,
        )
        plot.add_glyph(source, borders)
        plot.add_tools(HoverTool(tooltips=tooltips))
        return plot
