from __future__ import unicode_literals, absolute_import
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    Line,
    LinearAxis,
    Patches,
    Plot,
    Range1d,
    Rect,
    SingleIntervalTicker,
    TapTool,
    Text,
    Triangle,
)
from bokeh.plotting import vplot, hplot

from .chart_constants import (
    PLOT_FORMATS, ORANGE, BLUE, DARK_GRAY, AXIS_FORMATS, ORANGE_SHADOW,
    FONT_PROPS_SM, FONT_PROPS_MD, FONT_PROPS_LG, GREEN
)


def construct_map(source, fill_string='water_color', selected_color=ORANGE):
    assert isinstance(source, ColumnDataSource), "Require ColumnDataSource"

    # Plot and axes
    x_start, x_end = (-18, 55)
    y_start, y_end = (-35, 38)
    xdr = Range1d(x_start, x_end)
    ydr = Range1d(y_start, y_end)

    aspect_ratio = (x_end - x_start) / (y_end - y_start)
    plot_height = 600
    plot_width = int(plot_height * aspect_ratio)
    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=plot_width,
        plot_height=plot_height,
        min_border=0,
        **PLOT_FORMATS
    )

    borders = Patches(
        xs='xs', ys='ys',
        fill_color=fill_string, fill_alpha=1,
        line_color="#FFFFFF", line_width=1,
    )
    selected_borders = Patches(
        xs='xs', ys='ys',
        fill_color=fill_string, fill_alpha=1,
        line_color=selected_color, line_width=3,
    )

    plot.add_glyph(source, borders, selection_glyph=selected_borders, nonselection_glyph=borders)  # nopep8
    return plot


def construct_water_map(source):
    return construct_map(source, fill_string='wat_color')


def construct_san_map(source):
    return construct_map(source, fill_string='san_color', selected_color=DARK_GRAY)  # nopep8


def construct_water_map_tools(source):
    plot = construct_water_map(source)
    tooltips = "<span class='tooltip-text year'>@year</span>"
    tooltips += "<span class='tooltip-text country'>@name</span>"
    tooltips += "<span class='tooltip-text value'>@wat_value %</span>"
    plot.add_tools(HoverTool(tooltips=tooltips))
    plot.add_tools(TapTool())
    return plot


def construct_san_map_tools(source):
    plot = construct_san_map(source)
    tooltips = "<span class='tooltip-text year'>@year</span>"
    tooltips += "<span class='tooltip-text country'>@name</span>"
    tooltips += "<span class='tooltip-text value'>@san_value %</span>"
    plot.add_tools(HoverTool(tooltips=tooltips))
    plot.add_tools(TapTool())
    return plot


def construct_text_box(source, value_string, color_string, bar_color):
    # Plot and axes
    xdr = Range1d(0, 220)
    ydr = Range1d(0, 120)

    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=250,
        plot_height=120,
        min_border=0,
        **PLOT_FORMATS
    )
    # Add the writing
    country = Text(x=5, y=50, text='name', **FONT_PROPS_MD)
    percent = Text(x=15, y=10, text=value_string, text_color=color_string, **FONT_PROPS_LG)  # nopep8
    percent_sign = Text(x=69, y=10, text=['%'], text_color=color_string, **FONT_PROPS_LG)  # nopep8
    line_one = Text(x=90, y=28, text=['of people had'], **FONT_PROPS_SM)
    line_two_p1 = Text(x=90, y=14, text=['access in'], **FONT_PROPS_SM)
    line_two_p2 = Text(x=136, y=14, text='year', **FONT_PROPS_SM)
    plot.add_glyph(source, Text(), selection_glyph=country)
    plot.add_glyph(source, Text(), selection_glyph=percent)
    plot.add_glyph(source, Text(), selection_glyph=percent_sign)
    plot.add_glyph(line_one)
    plot.add_glyph(line_two_p1)
    plot.add_glyph(source, Text(), selection_glyph=line_two_p2)

    # Add the orange box with year
    shadow = Triangle(x=150, y=109, size=25, fill_color=ORANGE_SHADOW, line_color=None)  # nopep8
    plot.add_glyph(shadow)
    # Add the blue bar
    rect = Rect(x=75, y=99, width=150, height=5, fill_color=bar_color, line_color=None)  # nopep8
    plot.add_glyph(rect)
    box = Rect(x=200, y=100, width=100, height=40, fill_color=ORANGE, line_color=None)  # nopep8
    plot.add_glyph(box)
    year = Text(x=160, y=85, text='year', text_font_size='18pt', text_color="#FFFFF", text_font_style="bold")  # nopep8
    plot.add_glyph(source, Text(), selection_glyph=year)

    return plot


def construct_water_text(source):
    plot = construct_text_box(source, 'wat_value', 'wat_color', BLUE)
    return plot


def construct_san_text(source):
    plot = construct_text_box(source, 'san_value', 'san_color', GREEN)
    return plot


def construct_line(source, value_string, line_color=BLUE):
    xdr = Range1d(1990, 2013)
    ydr = Range1d(0, 100)
    line_plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=250,
        plot_height=150,
        min_border_top=10,
        min_border_left=50,
        **PLOT_FORMATS
    )
    xaxis = LinearAxis(SingleIntervalTicker(interval=50), **AXIS_FORMATS)
    yaxis = LinearAxis(SingleIntervalTicker(interval=10), **AXIS_FORMATS)
    line_plot.add_layout(xaxis, 'left')
    line_plot.add_layout(yaxis, 'below')

    line = Line(
        x='year', y=value_string,
        line_width=5, line_cap="round",
        line_color=line_color,
    )
    line_plot.add_glyph(source, line)

    return line_plot


def construct_water_line(source):
    plot = construct_line(source, 'wat_value', BLUE)
    return plot


def construct_san_line(source):
    plot = construct_line(source, 'san_value', GREEN)
    return plot


def construct_key(palette):
    xdr = Range1d(0, 250)
    ydr = Range1d(0, 50)

    plot = Plot(
        x_range=xdr,
        y_range=ydr,
        title="",
        plot_width=250,
        plot_height=50,
        min_border=0,
        **PLOT_FORMATS
    )

    for index, color in enumerate(palette):
        width = 19
        rect = Rect(
            x=((width * index) + 40), y=40,
            width=width, height=10,
            fill_color=color, line_color='white'
        )
        plot.add_glyph(rect)

    zero = Text(x=30, y=15, text=['0 %'], **FONT_PROPS_SM)
    hundred = Text(x=190, y=15, text=['100 %'], **FONT_PROPS_SM)
    plot.add_glyph(zero)
    plot.add_glyph(hundred)

    return plot


def layout_components(map_plot, line_plot, text_box, key):
    detail = vplot(text_box, line_plot, key)
    mapbox = vplot(map_plot)
    composed = hplot(mapbox, detail)
    return composed
