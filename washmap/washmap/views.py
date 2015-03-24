from django.views.generic import TemplateView

from bokeh.charts import Line
from pandas import DataFrame
from main.utils import BokehScriptComponents

from stats.models import StatValue


class ChartView(TemplateView):
    template_name = 'washmap/chart.html'


class GettingStarted(TemplateView):
    template_name = 'washmap/reveal_with_bokeh_css.html'

    def get_context_data(self, *args, **kwargs):
        context = super(GettingStarted, self).get_context_data(*args, **kwargs)
        line_basic = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_basic(),
            elementid='line_basic',
            min_width=300
        )
        line_args = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_args(),
            elementid='line_args',
            min_width=300
        )
        line_tweaks = BokehScriptComponents(
            plot_object=WaterAccessPercentLineChart().construct_plot_tweaks(),
            elementid='line_tweaks',
            min_width=300
        )
        context.update(
            figures=[line_basic, line_args, line_tweaks],
            title="Getting started"
        )
        return context


class WaterAccessPercentLineChart(object):
    def get_data(self):
        query = StatValue.objects.filter(country__name='Angola')
        query = query.filter(description__code='WNTI_%')
        query = query.values('year', 'value')
        df = DataFrame.from_records(query, index='year', coerce_float=True)
        df.to_pickle('/home/bird/Dev/birdsarah/pycon_2015_bokeh_talk/presentation/pickles/basic_line_data.pickle')
        return df

    def construct_plot_basic(self):
        data = self.get_data()
        plot = Line(data)
        return plot

    def construct_plot_args(self):
        data = self.get_data()
        plot = Line(
            data, tools="",
            xlabel=None, ylabel=None, xgrid=None, ygrid=None,
            title="% access to an improved water source"
        )
        return plot

    def construct_plot_tweaks(self):
        data = self.get_data()
        plot = Line(
            data, tools="",
            xlabel=None, ylabel=None, xgrid=None, ygrid=None,
            title="% access to an improved water source"
        )
        plot.toolbar_location = None
        plot.renderers[2].glyph.line_width = 5
        plot.renderers[2].glyph.line_cap = 'round'
        return plot
