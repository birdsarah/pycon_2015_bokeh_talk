from bokeh.models import ColumnDataSource
from bokeh.properties import Instance
from bokeh.models.widgets import Slider, VBox
from bokeh.models.widgets import Tabs, Panel

from washmap.map_data import (
    get_water_data_with_countries,
    get_sanitation_data_with_countries,
    get_frame_for_country,
)
from washmap.water_map import (
    construct_map,
    construct_line_single,
    construct_text_box,
    layout_components,
)
from washmap.chart_constants import BLUE, GREEN


class WashmapApp(VBox):
    parent_model = "VBox"
    js_model = "WashmapApp"

    year = Instance(Slider)

    wat_source = Instance(ColumnDataSource)
    san_source = Instance(ColumnDataSource)
    wat_source_single = Instance(ColumnDataSource)
    san_source_single = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        obj = cls()

        obj.year = Slider(
            title="Year", name='year',
            value=1990, start=1990, end=2012, step=1
        )

        country = 'South Africa'
        wat_data = get_water_data_with_countries()
        wat_data_single = get_frame_for_country(wat_data, country)
        san_data = get_sanitation_data_with_countries()
        san_data_single = get_frame_for_country(san_data, country)

        obj.wat_source = ColumnDataSource(wat_data)
        obj.wat_source_single = ColumnDataSource(wat_data_single)
        obj.san_source = ColumnDataSource(san_data)
        obj.san_source_single = ColumnDataSource(san_data_single)

        wat_plot = construct_map(obj.wat_source)
        wat_line = construct_line_single(obj.wat_source_single)
        wat_text = construct_text_box(obj.wat_source_single, bar_color=BLUE)

        san_plot = construct_map(obj.san_source)
        san_line = construct_line_single(obj.san_source_single)
        san_text = construct_text_box(obj.san_source_single, bar_color=GREEN)

        tabs = Tabs(
            tabs=[
                Panel(
                    title="Water",
                    child=layout_components(wat_plot, wat_line, wat_text)
                ),
                Panel(
                    title="Sanitation",
                    child=layout_components(san_plot, san_line, san_text)
                )
            ]
        )

        obj.children = [tabs, obj.year]

        return obj
