from __future__ import unicode_literals, absolute_import

from bokeh.embed import components, Resources
from django.conf import settings
from django.views.generic import TemplateView

from main.utils import BokehScriptComponents, app_document_no_tag


from .washmap_static import (
    make_washmap_map,
    make_washmap_map_tools,
    make_washmap_map_tools_linked,
    make_washmap_map_tools_linked_tabbed,
    make_washmap_all
)
from .washmap_app import WashmapApp
from .charts_demos import make_line_chart


class WashMapStaticView(TemplateView):
    template_name = 'washmap/chart.html'
    name = 'base'

    def get_context_data(self, *args, **kwargs):
        context = super(WashMapStaticView, self).get_context_data(*args, **kwargs)  # nopep8
        water_map_static = BokehScriptComponents(
            plot_object=self.make_plot(),
            elementid='water_map_static',
            min_width=200
        )
        context.update(
            figures=[water_map_static],
            title="Washmap",
            name=self.name
        )
        return context


class WashMapStaticMapView(WashMapStaticView):
    name = 'map'

    def make_plot(self):
        plot = make_washmap_map()
        return plot


class WashMapStaticMapToolsView(WashMapStaticView):

    def make_plot(self):
        plot = make_washmap_map_tools()
        return plot


class WashMapStaticMapToolsLinkedView(WashMapStaticView):
    def make_plot(self):
        plot = make_washmap_map_tools_linked()
        return plot


class WashMapStaticMapToolsLinkedTabbedView(WashMapStaticView):
    def make_plot(self):
        plot = make_washmap_map_tools_linked_tabbed()
        return plot


class WashMapStaticAllView(WashMapStaticView):
    def make_plot(self):
        plot = make_washmap_all()
        return plot


class WashMapServerView(TemplateView):
    template_name = 'washmap/chart_from_server.html'

    @app_document_no_tag('washmap', settings.BOKEH_URL)
    def make_app(self):
        app = WashmapApp.create()
        return app

    def get_context_data(self, *args, **kwargs):
        context = super(WashMapServerView, self).get_context_data(*args, **kwargs)  # nopep8
        applet = self.make_app()
        applet_dict = {
            'elementid': 'washmap',
            'root_url': applet._root_url,
            'docid': applet._docid,
            'modelid': applet._id,
            'js_model': applet.js_model,
            'modulename': applet.js_model,
            'classname': applet.js_model,
            'parentname': applet.parent_model,
        }
        context.update(
            applet=applet_dict
        )
        return context


class LineStaticView(TemplateView):
    template_name = 'washmap/chart_basic_embed.html'

    def get_context_data(self, *args, **kwargs):
        context = super(LineStaticView, self).get_context_data(*args, **kwargs)
        line_chart = make_line_chart()
        embed_script, embed_div = components(line_chart, Resources())
        context.update(
            embed_div=embed_div,
            embed_script=embed_script
        )
        return context
