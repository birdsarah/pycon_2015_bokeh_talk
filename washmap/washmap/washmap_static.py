from bokeh.models import (
    ColumnDataSource,
)
from bokeh.models.widgets import Tabs, Panel
from bokeh.plotting import vplot


from .map_data import (
    get_water_data_with_countries,
    get_sanitation_data_with_countries,
)
from .water_map import (
    construct_map,
    construct_line_single,
    construct_text_box,
    layout_components,
)
from .chart_constants import (
    BLUE,
    GREEN
)


def get_frame_for_country(frame, country):
    return frame[frame.name == country]


def make_washmap():
    wat_data = get_water_data_with_countries()
    san_data = get_sanitation_data_with_countries()
    country = 'South Africa'

    wat_source = ColumnDataSource(wat_data)
    wat_plot = construct_map(wat_source)

    wat_single_country = get_frame_for_country(wat_data, country)
    wat_source_single = ColumnDataSource(wat_single_country)
    wat_line = construct_line_single(wat_source_single)
    wat_text = construct_text_box(wat_source_single, bar_color=BLUE)

    san_source = ColumnDataSource(san_data)
    san_plot = construct_map(san_source)

    san_single_country = get_frame_for_country(san_data, country)
    san_source_single = ColumnDataSource(san_single_country)
    san_line = construct_line_single(san_source_single)
    san_text = construct_text_box(san_source_single, bar_color=GREEN)

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

    return vplot(tabs)
