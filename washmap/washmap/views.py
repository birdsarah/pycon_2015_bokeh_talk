from django.views.generic import TemplateView

from main.utils import BokehScriptComponents


class Line(object):
    def construct_plot(self):
        pass


class LineView(TemplateView):
    template_name = 'washmap/charts.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LineView, self).get_context_data(*args, **kwargs)
        line = BokehScriptComponents(
            plot_object=Line().construct_plot(),
            elementid='line'
        )
        context.update(
            line=line,
            figures=[line]
        )
        return context
