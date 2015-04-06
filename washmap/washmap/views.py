from __future__ import unicode_literals, absolute_import

from django.conf import settings
from django.views.generic import TemplateView

from main.utils import BokehScriptComponents, app_document_no_tag


from .washmap_static import make_washmap
from .washmap_app import WashmapApp


class WashMapStaticView(TemplateView):
    template_name = 'washmap/chart.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WashMapStaticView, self).get_context_data(*args, **kwargs)  # nopep8
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
