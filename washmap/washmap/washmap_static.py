from bokeh.models import (
    ColumnDataSource,
)
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import vplot, hplot


from .map_data import get_data_with_countries
from .water_map import (
    construct_water_map,
    construct_water_map_tools,
    construct_san_map,
    construct_san_map_tools,
    construct_line,
    construct_water_text,
    construct_san_text,
    construct_key,
    layout_components,
)
from .chart_constants import (
    BLUE,
    GREEN,
    WATER_COLOR_RANGE,
    SANITATION_COLOR_RANGE,
)


def get_frame_for_country(frame, country):
    return frame[frame.name == country]


def make_washmap_map():
    data = get_data_with_countries()
    source = ColumnDataSource(data)
    wat_map = construct_water_map(source)
    wat_key = construct_key(WATER_COLOR_RANGE)
    return hplot(vplot(wat_map), vplot(wat_key))


def make_washmap_map_tools():
    data = get_data_with_countries()
    source = ColumnDataSource(data)
    wat_map = construct_water_map_tools(source)
    wat_key = construct_key(WATER_COLOR_RANGE)
    return hplot(vplot(wat_map), vplot(wat_key))


def make_washmap_map_tools_linked():
    data = get_data_with_countries()
    source = ColumnDataSource(data)
    wat_map = construct_water_map_tools(source)
    wat_text = construct_water_text(source)
    wat_key = construct_key(WATER_COLOR_RANGE)
    return hplot(vplot(wat_map), vplot(wat_text, wat_key))


def make_washmap_map_tools_linked_tabbed():
    pass


def make_washmap_all():
    data = get_data_with_countries()
    country = 'South Africa'

    source = ColumnDataSource(data)

    wat_data_text = get_frame_for_country(data, country)
    wat_source_text = ColumnDataSource(wat_data_text)

    year_range = [str(x) for x in range(1990, 2013)]
    wat_data_line = wat_data_text[year_range].transpose()
    wat_data_line.columns = ['value']
    wat_data_line = wat_data_line[wat_data_line['value'] > 0]
    wat_source_line = ColumnDataSource(wat_data_line)

    wat_plot = construct_map(wat_source)
    wat_line = construct_line(wat_source_line)
    wat_text = construct_text_box(wat_source_text, bar_color=BLUE)
    wat_key = construct_key(WATER_COLOR_RANGE)

    san_source = ColumnDataSource(san_data)

    san_data_text = get_frame_for_country(san_data, country)
    san_source_text = ColumnDataSource(san_data_text)

    san_data_line = san_data_text[year_range].transpose()
    san_data_line.columns = ['value']
    san_data_line = san_data_line[san_data_line['value'] > 0]
    san_source_line = ColumnDataSource(san_data_line)

    san_plot = construct_map(san_source)
    san_line = construct_line(san_source_line, line_color=GREEN)
    san_text = construct_text_box(san_source_text, bar_color=GREEN)
    san_key = construct_key(SANITATION_COLOR_RANGE)

    tabs = Tabs(
        tabs=[
            Panel(
                title="Water",
                child=layout_components(wat_plot, wat_line, wat_text, wat_key)
            ),
            Panel(
                title="Sanitation",
                child=layout_components(san_plot, san_line, san_text, san_key)
            )
        ]
    )

    return vplot(tabs)
