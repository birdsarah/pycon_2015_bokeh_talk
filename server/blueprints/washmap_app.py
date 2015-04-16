from bokeh.models import ColumnDataSource
from bokeh.properties import Instance
from bokeh.models.widgets import Slider, VBox, TextInput
from pandas import DataFrame

import logging
log = logging.getLogger(__name__)

# update_active_data and get_frame_for_country are exact copies of
# methods used in client app (under map_data.py)

from numpy import where, take
WATER_COLOR_RANGE = ["#8c9494", "#8398a2", "#7c9baa", "#73a1b4", "#6aa6bd", "#62abc7", "#5aafd0", "#52b4d9", "#49bae4", "#3fc0f0"]  # nopep8
SANITATION_COLOR_RANGE = ["#d45500", "#da670f", "#eb7e1f", "#eb941f", "#ebb01f", "#f2c83d", "#d3cc4f", "#86c26f", "#4db181", "#15b598"]  # nopep8
GRAY = "#CCCCCC"


class WashmapApp(VBox):
    year = Instance(Slider)

    current_country = Instance(TextInput)

    source = Instance(ColumnDataSource)
    wat_all = Instance(ColumnDataSource)
    san_all = Instance(ColumnDataSource)
    line_source = Instance(ColumnDataSource)

    def setup_events(self):
        self.year.on_change('value', self, 'change_year')
        self.source.on_change('selected', self, 'change_line_source')

    def change_year(self, obj, attrname, old, new):
        year = str(self.year.value)
        data = DataFrame(self.source.data)
        new_data = self._update_data_for_new_year(data, year)
        self.source.data = ColumnDataSource(new_data).data

    def change_line_source(self, obj, attrname, old, new):
        if new == []:
            # if no country selected, default to Morocco
            new = [30]
            self.source.selected = new
        country_name = take(obj.data['name'], new)
        # np gives us an array, assuming only one country
        country_name = country_name[0]
        new_line_data = self._get_line_data_for_country(country_name)
        self.line_source.data = ColumnDataSource(new_line_data).data

    def get_wat_san_dfs(self):
        wat_all_df = DataFrame(self.wat_all.data)
        wat_all_df = wat_all_df.drop('index', axis=1)
        san_all_df = DataFrame(self.san_all.data)
        san_all_df = san_all_df.drop('index', axis=1)
        return wat_all_df, san_all_df

    def _get_line_data_for_country(self, country_name):
        # filter wat and san to get just that country
        wat_all_df, san_all_df = self.get_wat_san_dfs()
        new_wat_data = wat_all_df[wat_all_df.name == country_name]
        new_san_data = san_all_df[san_all_df.name == country_name]
        new_data = new_wat_data.merge(new_san_data, on='year')
        return new_data

    def _update_data_for_new_year(self, data, year):
        data = data.drop(
            ['wat_value', 'san_value', 'wat_color', 'san_color'], axis=1
        )
        data.year = year
        wat_all_df, san_all_df = self.get_wat_san_dfs()
        data = data.merge(wat_all_df, how='left')
        data = data.merge(san_all_df, how='left')
        data = data.fillna(-99)

        colored_df = self._color_data(data)
        colored_df.head()
        return colored_df

    def _color_data(self, data):
        def _get_color(value, palette):
            if value < 0:
                return GRAY
            index = int((value - 0.01) / 10)
            return palette[index]

        data['wat_color'] = data['wat_value'].apply(
            _get_color, args=([WATER_COLOR_RANGE])
        )
        data['san_color'] = data['san_value'].apply(
            _get_color, args=([SANITATION_COLOR_RANGE])
        )
        data['wat_value'] = where(data['wat_value'] < 0, '-', data['wat_value'])  # nopep8
        data['san_value'] = where(data['san_value'] < 0, '-', data['san_value'])  # nopep8
        return data
