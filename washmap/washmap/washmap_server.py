from __future__ import unicode_literals, absolute_import
from .map_data import (
    get_sanitation_data_with_countries,
    get_water_data_with_countries,
)
from .water_map import (
    construct_map,
)
from bokeh.models.widgets import Tabs, Panel, VBox
from bokeh.models import ColumnDataSource
from bokeh.properties import Instance
from bokeh.models.widgets import Slider, VBoxForm


class WashmapApp(VBox):
    parent_model = "VBox"
    js_model = "WashmapApp"

    inputs = Instance(VBoxForm)
    year = Instance(Slider)

    water_source = Instance(ColumnDataSource)
    sanitation_source = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        obj = cls()

        obj.year = Slider(
            title="Year", name='year',
            value=1990, start=1990, end=2012, step=1
        )

        water_data = get_water_data_with_countries()
        obj.water_source = ColumnDataSource(water_data)
        water_plot = construct_map(source=obj.water_source)

        san_data = get_sanitation_data_with_countries()
        obj.sanitation_source = ColumnDataSource(san_data)
        san_plot = construct_map(source=obj.sanitation_source)

        tabs = Tabs(
            tabs=[
                Panel(title="Water", child=water_plot),
                Panel(title="Sanitation", child=san_plot)
            ]
        )

        obj.children = [tabs, obj.year]

        return obj
