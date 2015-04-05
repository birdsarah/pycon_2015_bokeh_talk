from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import vplot

from .map_data import (
    get_water_data_with_countries,
    get_sanitation_data_with_countries,
)
from .water_map import (
    construct_map,
    construct_line,
    construct_text_box,
    layout_components,
)
from .chart_constants import (
    WATER_COLOR_RANGE,
    SANITATION_COLOR_RANGE,
    BLUE,
    GREEN
)


def make_washmap():
    water_data = get_water_data_with_countries()
    water_plot = construct_map(data=water_data)
    water_line = construct_line(data=water_data, palette=WATER_COLOR_RANGE)
    water_text = construct_text_box(data=water_data, bar_color=BLUE)

    san_data = get_sanitation_data_with_countries()
    san_plot = construct_map(data=san_data)
    san_line = construct_line(data=san_data, palette=SANITATION_COLOR_RANGE)
    san_text = construct_text_box(data=san_data, bar_color=GREEN)

    tabs = Tabs(
        tabs=[
            Panel(
                title="Water",
                child=layout_components(water_plot, water_line, water_text)
            ),
            Panel(
                title="Sanitation",
                child=layout_components(san_plot, san_line, san_text)
            )
        ]
    )

    return vplot(children=[tabs])
