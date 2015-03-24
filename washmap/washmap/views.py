from django.views.generic import TemplateView

from bokeh.charts import Line
from pandas import DataFrame
from main.utils import BokehScriptComponents


class LineView(TemplateView):
    template_name = 'washmap/chart.html'

#    def get_data(self):
#        query = WASHMapData.objects.all().values(
#            'country__name',
#            'water_initial',
#            'water_increase',
#        )
#        df = DataFrame.from_records(query, coerce_float=True)
#        return df
#
    def get_context_data(self, *args, **kwargs):
        context = super(LineView, self).get_context_data(*args, **kwargs)
#        line = BokehScriptComponents(
#            plot_object=Line().construct_plot(),
#            elementid='line'
#        )
#        context.update(
#            figures=[line]
#        )
        return context
