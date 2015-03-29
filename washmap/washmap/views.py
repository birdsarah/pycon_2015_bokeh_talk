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
from main.utils import BokehScriptComponents, app_document_no_tag

from stats.models import StatValue
from .chart_constants import PLOT_FORMATS, AXIS_FORMATS, LINE_FORMATS
from .water_map import make_washmap

class WashMapStaticView(TemplateView):
    template_name = 'washmap/chart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WashMapStaticView, self).get_context_data(*args, **kwargs)
        water_map_static = BokehScriptComponents(
            plot_object=make_washmap(),
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
