from __future__ import unicode_literals, absolute_import

from django.views.generic import TemplateView

from bokeh.charts import Line
from bokeh.models import (
    ColumnDataSource,
    Range1d,
    Plot,
    LinearAxis,
)
from pandas import DataFrame
from main.utils import BokehScriptComponents

from stats.models import StatValue
from .chart_constants import PLOT_FORMATS, AXIS_FORMATS, LINE_FORMATS
from .water_map import WaterAccessMap


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
