FONT = "News Cycle"
FONT_SIZE = "20pt"
WATER_COLOR_RANGE = ["#8c9494", "#8398a2", "#7c9baa", "#73a1b4", "#6aa6bd", "#62abc7", "#5aafd0", "#52b4d9", "#49bae4", "#3fc0f0"]
SANITATION_COLOR_RANGE = ["#d45500", "#da670f", "#eb7e1f", "#eb941f", "#ebb01f", "#f2c83d", "#d3cc4f", "#86c26f", "#4db181", "#15b598"]
NODATA_COLOR = "#eeeeee"
BLUE = WATER_COLOR_RANGE[5]
LIGHT_BLUE = WATER_COLOR_RANGE[9]
GREEN = "#43C4AD"
GRAY = "#CCCCCC"
DARK_GRAY = "#6B6B73"
ORANGE = "#FFA500"
ORANGE_SHADOW = "#D48702"
AXIS_FORMATS = dict(
    minor_tick_in=None,
    minor_tick_out=None,
    major_tick_in=None,
    major_label_text_font=FONT,
    major_label_text_font_size="10pt",
    major_label_text_font_style="bold",
    axis_label_text_font=FONT,
    axis_label_text_font_size="10pt",

    axis_line_color=GRAY,
    major_tick_line_color=GRAY,
    major_label_text_color=DARK_GRAY,

    major_tick_line_cap="round",
    axis_line_cap="round",
    axis_line_width=3,
    major_tick_line_width=3,
)
PLOT_FORMATS = dict(
    toolbar_location=None,
    outline_line_color="#FFFFFF",
    title_text_font=FONT,
    title_text_align='left',
    title_text_color=BLUE,
    title_text_baseline='top',
)
LINE_FORMATS = dict(
    line_width=5,
    line_cap='round',
    line_alpha=0.8,
    line_color=BLUE,
)
FONT_PROPS_SM = dict(
    text_color=DARK_GRAY,
    text_font=FONT,
    text_font_style="normal",
    text_font_size='10pt',
)
FONT_PROPS_MD = dict(
    text_color=DARK_GRAY,
    text_font=FONT,
    text_font_style="normal",
    text_font_size='18pt',
)
FONT_PROPS_LG = dict(
    text_font=FONT,
    text_font_style="bold",
    text_font_size='23pt',
)
