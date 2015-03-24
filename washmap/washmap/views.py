from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from bokeh.charts import Line
from bokeh.models import (
    ColumnDataSource,
    Range1d,
    Plot,
    LinearAxis,
    Patches,
    HoverTool,
)
from bokeh.palettes import brewer
from pandas import DataFrame, merge
from main.utils import BokehScriptComponents, build_coords_lists

from country.models import Country
from stats.models import StatValue

FONT = "News Cycle"
FONT_SIZE = "20px"
BLUE = "#2875A7"
GRAY = "#CCCCCC"
AXIS_FORMATS = dict(
    minor_tick_in=None,
    minor_tick_out=None,
    major_tick_in=None,
    major_tick_out=None,
    major_label_text_font=FONT,
    major_label_text_font_size=FONT_SIZE,
    axis_label_text_font=FONT,
    axis_label_text_font_size=FONT_SIZE,
    axis_line_color=None
)
PLOT_FORMATS = dict(
    toolbar_location=None,
    outline_line_color=None,
    title_text_font=FONT,
    title_text_align='left',
    title_text_color=BLUE,
    title_text_baseline='top',
)
LINE_FORMATS = dict(
    line_width=5,
    line_cap='round',
    line_alpha=0.8,
    line_color=BLUE,
)


class ChartView(TemplateView):
    template_name = 'washmap/chart.html'


class WashMapView(TemplateView):
    template_name = 'washmap/chart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WashMapView, self).get_context_data(*args, **kwargs)
        water_map_static = BokehScriptComponents(
            plot_object=WaterAccessMap().construct_static(),
            elementid='water_map_static',
            min_width=600
        )
        context.update(
            figures=[
                water_map_static
            ],
            title="Washmap"
        )
        return context


class GettingStarted(TemplateView):
    template_name = 'washmap/reveal_with_bokeh_css.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GettingStarted, self).get_context_data(*args, **kwargs)
        chart_basic = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_basic(),
            elementid='chart_basic',
            min_width=300
        )
        chart_args = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_args(),
            elementid='chart_args',
            min_width=300
        )
        chart_tweaks = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_tweaks(),
            elementid='chart_tweaks',
            min_width=300
        )
        chart_manual = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_manually(),  # nopep8
            elementid='chart_manual',
            min_width=300
        )
        water_map_static = BokehScriptComponents(
            plot_object=WaterAccessMap().construct_static(),
            elementid='water_map_static',
            min_width=600
        )
        context.update(
            figures=[
                chart_basic,
                chart_args,
                chart_tweaks,
                chart_manual,
                water_map_static
            ],
            title="Components"
        )
        return context


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


class WaterAccessPercentLineChart(object):
    def get_data(self):
        query = StatValue.objects.filter(country__name='Algeria')
        query = query.filter(description__code='WNTI_%')
        query = query.values('year', 'value')
        df = DataFrame.from_records(query, index='year', coerce_float=True)
        df.to_pickle('/home/bird/Dev/birdsarah/pycon_2015_bokeh_talk/presentation/pickles/basic_line_data.pickle')  # nopep8
        return df

    def construct_plot_basic(self):
        data = self.get_data()
        chart = Line(data)
        return chart

    chart_options = dict(
        tools="", palette=["#2875A7"],
        xlabel=None, ylabel=None, xgrid=None, ygrid=None,
        title="% access to an improved water source"
    )

    def construct_plot_args(self):
        data = self.get_data()
        chart = Line(data, **self.chart_options)
        return chart

    def construct_plot_tweaks(self):
        data = self.get_data()
        chart = Line(data, **self.chart_options)
        chart.toolbar_location = None
        chart.renderers[2].glyph.line_width = 5
        chart.renderers[2].glyph.line_cap = 'round'
        chart.toolbar_location = None
        chart.outline_line_color = None
        return chart

    def construct_plot_manually(self):
        data = self.get_data()
        source = ColumnDataSource(data)

        # Plot and axes
        xdr = Range1d(1990, 2012)
        ydr = Range1d(0, 100)

        plot = Plot(
            x_range=xdr,
            y_range=ydr,
            plot_width=1000,
            plot_height=600,
            title="% Access to improved water source.",
            **PLOT_FORMATS
        )
        x_axis = LinearAxis(**AXIS_FORMATS)
        y_axis = LinearAxis(axis_label="%", major_label_standoff=50, **AXIS_FORMATS)  # nopep8
        plot.add_layout(x_axis, 'below')
        plot.add_layout(y_axis, 'left')

        from bokeh.models.glyphs import Line
        line = Line(x="year", y="value", **LINE_FORMATS)
        plot.add_glyph(source, line)
        return plot
