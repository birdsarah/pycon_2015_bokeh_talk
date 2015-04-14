from bokeh.models import ColumnDataSource
from bokeh.properties import Instance
from bokeh.models.widgets import Slider, VBox, TextInput

import logging
log = logging.getLogger(__name__)

# update_active_data and get_frame_for_country are exact copies of
# methods used in client app (under map_data.py)

from numpy import where
WATER_COLOR_RANGE = ["#8c9494", "#8398a2", "#7c9baa", "#73a1b4", "#6aa6bd", "#62abc7", "#5aafd0", "#52b4d9", "#49bae4", "#3fc0f0"]  # nopep8
SANITATION_COLOR_RANGE = ["#d45500", "#da670f", "#eb7e1f", "#eb941f", "#ebb01f", "#f2c83d", "#d3cc4f", "#86c26f", "#4db181", "#15b598"]  # nopep8
GRAY = "#CCCCCC"


def update_active_data(data, active_year, palette_name=None):
    # Default to water
    palette = WATER_COLOR_RANGE
    if palette_name == 'sanitation':
        palette = SANITATION_COLOR_RANGE

    def _get_color(value):
        if value < 0:
            return GRAY
        index = int(value / 10)
        return palette[index]

    data['active_year'] = active_year
    data['active_year_value'] = data[active_year]
    data['color_for_active_year'] = data[active_year].apply(_get_color)
    data['active_year_value'] = where(data['active_year_value'] < 0, '-', data['active_year_value'])  # nopep8
    return data


def get_frame_for_country(frame, country_name):
    return frame[frame.name == country_name]


class WashmapApp(VBox):
    year = Instance(Slider)

    current_country = Instance(TextInput)

    wat_source_map = Instance(ColumnDataSource)
    san_source_map = Instance(ColumnDataSource)
    wat_source_line = Instance(ColumnDataSource)
    san_source_line = Instance(ColumnDataSource)
    wat_source_text = Instance(ColumnDataSource)
    san_source_text = Instance(ColumnDataSource)

    def setup_events(self):
        self.year.on_change('value', self, 'change_year')
        self.wat_source_map.on_change('selected', self, 'change_country_wat')
        self.san_source_map.on_change('selected', self, 'change_country_san')

    def change_year(self, obj, attrname, old, new):
        year = str(self.year.value)
        wat_data, san_data = self._set_map_source(year)
        self._set_text_source(wat_data, san_data)

    def change_country_wat(self, obj, attrname, old, new):
        if new == []:
            new = [30]
            self.wat_source_map.selected = new
        self.change_country(obj, attrname, old, new)
        self.san_source_map.selected = self.wat_source_map.selected

    def change_country_san(self, obj, attrname, old, new):
        if new == []:
            new = [30]
            self.san_source_map.selected = new
        self.change_country(obj, attrname, old, new)
        self.wat_source_map.selected = self.san_source_map.selected

    def change_country(self, obj, attrname, old, new):
        source_index = new[-1]
        country_name = obj.data['name'][source_index]
        wat_df, san_df = self.get_dfs()
        wat_data_text, san_data_text = self._set_text_source(wat_df, san_df)
        self._set_line_source(wat_data_text, san_data_text)
        # select the countries
        self.current_country.value = country_name

    def _set_map_source(self, year):
        wat_df, san_df = self.get_dfs()
        wat_data = update_active_data(wat_df, year, palette_name='water')
        san_data = update_active_data(san_df, year, palette_name='sanitation')

        self.wat_source_map.data = ColumnDataSource(wat_data).data
        self.san_source_map.data = ColumnDataSource(san_data).data
        return wat_data, san_data

    def _set_text_source(self, wat_data, san_data):
        wat_data_text, san_data_text = self.get_single_dfs(
            wat_data, san_data, self.current_country.value
        )
        self.wat_source_text.data = ColumnDataSource(wat_data_text).data
        self.san_source_text.data = ColumnDataSource(san_data_text).data
        return wat_data_text, san_data_text

    def _set_line_source(self, wat_data_text, san_data_text):
        year_range = [str(x) for x in range(1990, 2013)]

        wat_data_line = wat_data_text[year_range].transpose()
        wat_data_line.columns = ['value']
        wat_data_line = wat_data_line[wat_data_line['value'] > 0]

        san_data_line = san_data_text[year_range].transpose()
        san_data_line.columns = ['value']
        san_data_line = san_data_line[san_data_line['value'] > 0]

        self.wat_source_line.data = ColumnDataSource(wat_data_line).data
        self.san_source_line.data = ColumnDataSource(san_data_line).data
        return wat_data_line, san_data_line

    def get_dfs(self):
        wat_data = self.wat_source_map.to_df()
        san_data = self.san_source_map.to_df()
        return wat_data, san_data

    def get_single_dfs(self, wat_data, san_data, country_id):
        wat_data_single = get_frame_for_country(wat_data, country_id)
        san_data_single = get_frame_for_country(san_data, country_id)
        return wat_data_single, san_data_single
