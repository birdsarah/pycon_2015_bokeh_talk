from bokeh.models import ColumnDataSource
from bokeh.properties import Instance
from bokeh.models.widgets import Slider, VBox, Tabs, Panel, TextInput

from washmap.map_data import (
    get_data_with_countries,
    get_frame_for_country,
    get_wat_stats_all_years,
    get_san_stats_all_years,
)
from washmap.water_map import (
    construct_water_map,
    construct_water_map_tools,
    construct_san_map,
    construct_san_map_tools,
    construct_water_line,
    construct_san_line,
    construct_water_text,
    construct_san_text,
    construct_key,
    layout_components,
)
from .charts_demos import get_line_data
from washmap.chart_constants import (
    BLUE, GREEN, DARK_GRAY, WATER_COLOR_RANGE, SANITATION_COLOR_RANGE
)


class WashmapApp(VBox):
    parent_model = "VBox"
    js_model = "WashmapApp"

    year = Instance(Slider)

    source = Instance(ColumnDataSource)
    wat_all = Instance(ColumnDataSource)
    san_all = Instance(ColumnDataSource)
    line_source = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        obj = cls()

        obj.year = Slider(
            title="Year", name='year',
            value=1990, start=1990, end=2012, step=1
        )
        wat_all_df = get_wat_stats_all_years()
        san_all_df = get_san_stats_all_years()
        data = get_data_with_countries(wat_all_df, san_all_df)
        source = ColumnDataSource(data)
        source.selected = [30]
        line_data = get_line_data('Morocco')
        line_source = ColumnDataSource(line_data)

        wat_map = construct_water_map_tools(source)
        wat_line = construct_water_line(line_source)
        wat_text = construct_water_text(source)
        wat_key = construct_key(WATER_COLOR_RANGE)
        san_map = construct_san_map_tools(source)
        san_line = construct_san_line(line_source)
        san_text = construct_san_text(source)
        san_key = construct_key(SANITATION_COLOR_RANGE)

        obj.source = source
        obj.line_source = line_source
        wat_all_df.year = wat_all_df.year.astype(str)
        san_all_df.year = san_all_df.year.astype(str)
        obj.wat_all = ColumnDataSource(wat_all_df)
        obj.san_all = ColumnDataSource(san_all_df)

        tabs = Tabs(
            tabs=[
                Panel(
                    title="Water",
                    child=layout_components(wat_map, wat_line, wat_text, wat_key)
                ),
                Panel(
                    title="Sanitation",
                    child=layout_components(san_map, san_line, san_text, san_key)
                )
            ]
        )

        obj.children = [tabs, obj.year]

        return obj
