from bokeh.models import ColumnDataSource
from bokeh.properties import Instance
from bokeh.models.widgets import Slider, VBox, Tabs, Panel, TextInput

from washmap.map_data_server import (
    get_water_data_with_countries,
    get_sanitation_data_with_countries,
    get_frame_for_country,
)
from washmap.water_map_server import (
    construct_map,
    construct_line,
    construct_text_box,
    construct_key,
    layout_components,
)
from washmap.chart_constants import (
    BLUE, GREEN, DARK_GRAY, WATER_COLOR_RANGE, SANITATION_COLOR_RANGE
)


class WashmapApp(VBox):
    parent_model = "VBox"
    js_model = "WashmapApp"

    year = Instance(Slider)

    current_country = Instance(TextInput)

    wat_source_map = Instance(ColumnDataSource)
    san_source_map = Instance(ColumnDataSource)
    wat_source_line = Instance(ColumnDataSource)
    san_source_line = Instance(ColumnDataSource)
    wat_source_text = Instance(ColumnDataSource)
    san_source_text = Instance(ColumnDataSource)

    @classmethod
    def create(cls):
        obj = cls()

        obj.year = Slider(
            title="Year", name='year',
            value=1990, start=1990, end=2012, step=1
        )
        country = 'Morocco'
        obj.current_country = TextInput(
            title="Country", name="country", value=country
        )

        year_range = [str(x) for x in range(1990, 2013)]
        wat_data = get_water_data_with_countries()
        san_data = get_sanitation_data_with_countries()
        wat_data_text = get_frame_for_country(wat_data, country)
        san_data_text = get_frame_for_country(san_data, country)
        wat_data_line = wat_data_text[year_range].transpose()
        wat_data_line.columns = ['value']
        wat_data_line = wat_data_line[wat_data_line['value'] > 0]

        san_data_line = san_data_text[year_range].transpose()
        san_data_line.columns = ['value']
        san_data_line = san_data_line[san_data_line['value'] > 0]

        obj.wat_source_map = ColumnDataSource(wat_data)
        obj.wat_source_map.selected = [30]
        obj.san_source_map = ColumnDataSource(san_data)
        obj.san_source_map.selected = [30]
        obj.wat_source_line = ColumnDataSource(wat_data_line)
        obj.san_source_line = ColumnDataSource(san_data_line)
        obj.wat_source_text = ColumnDataSource(wat_data_text)
        obj.san_source_text = ColumnDataSource(san_data_text)

        wat_plot = construct_map(obj.wat_source_map)
        wat_line = construct_line(obj.wat_source_line, line_color=BLUE)
        wat_text = construct_text_box(obj.wat_source_text, bar_color=BLUE)
        wat_key = construct_key(WATER_COLOR_RANGE)

        san_plot = construct_map(obj.san_source_map, selected_color=DARK_GRAY)
        san_line = construct_line(obj.san_source_line, line_color=GREEN)
        san_text = construct_text_box(obj.san_source_text, bar_color=GREEN)
        san_key = construct_key(SANITATION_COLOR_RANGE)

        tabs = Tabs(
            tabs=[
                Panel(
                    title="Water",
                    child=layout_components(wat_plot, wat_line, wat_text, wat_key)  # nopep8
                ),
                Panel(
                    title="Sanitation",
                    child=layout_components(san_plot, san_line, san_text, san_key)  # nopep8
                )
            ]
        )

        obj.children = [tabs, obj.year]

        return obj
