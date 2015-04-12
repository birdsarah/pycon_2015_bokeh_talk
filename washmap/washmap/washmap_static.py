from bokeh.models import (
    ColumnDataSource,
)
from bokeh.models.widgets import Tabs, Panel, Slider
from bokeh.plotting import vplot, hplot


from .map_data import get_data_with_countries
from .charts_demos import get_line_data
from .water_map import (
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
    data = get_data_with_countries()
    source = ColumnDataSource(data)
    source.selected = [30]
    wat_map = construct_water_map_tools(source)
    wat_text = construct_water_text(source)
    wat_key = construct_key(WATER_COLOR_RANGE)
    san_map = construct_san_map_tools(source)
    san_text = construct_san_text(source)
    san_key = construct_key(SANITATION_COLOR_RANGE)

    tabs = Tabs(
        tabs=[
            Panel(
                title="Water",
                child=hplot(vplot(wat_map), vplot(wat_text, wat_key))
            ),
            Panel(
                title="Sanitation",
                child=hplot(vplot(san_map), vplot(san_text, san_key))
            )
        ]
    )
    return vplot(tabs)


def make_washmap_all():
    data = get_data_with_countries()

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
    year = Slider(
        title="Year", name='year',
        value=1990, start=1990, end=2012, step=1
    )

    return vplot(tabs, year)
