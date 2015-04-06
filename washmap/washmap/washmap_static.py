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
    construct_line,
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

    wat_data_text = get_frame_for_country(wat_data, country)
    wat_source_text = ColumnDataSource(wat_data_text)
    wat_text = construct_text_box(wat_source_text, bar_color=BLUE)

    year_range = [str(x) for x in range(1990, 2013)]
    wat_data_line = wat_data_text[year_range].transpose()
    wat_data_line.columns = ['value']
    wat_data_line = wat_data_line[wat_data_line['value'] > 0]
    wat_source_line = ColumnDataSource(wat_data_line)
    wat_line = construct_line(wat_source_line)

    san_source = ColumnDataSource(san_data)
    san_plot = construct_map(san_source)

    san_data_text = get_frame_for_country(san_data, country)
    san_source_text = ColumnDataSource(san_data_text)
    san_text = construct_text_box(san_source_text, bar_color=GREEN)

    san_data_line = san_data_text[year_range].transpose()
    san_data_line.columns = ['value']
    san_data_line = san_data_line[san_data_line['value'] > 0]
    san_source_line = ColumnDataSource(san_data_line)
    san_line = construct_line(san_source_line, line_color=GREEN)

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
