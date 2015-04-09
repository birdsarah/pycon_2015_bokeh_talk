from bokeh.charts import Line
from .map_data import get_water_data_with_countries, get_frame_for_country

def get_line_data():
    country = 'South Africa'
    year_range = [str(x) for x in range(1990, 2013)]

    wat_data = get_water_data_with_countries()

    wat_data_text = get_frame_for_country(wat_data, country)
    wat_data_line = wat_data_text[year_range].transpose()
    wat_data_line.columns = ['value']
    wat_data_line = wat_data_line[wat_data_line['value'] > 0]
    return wat_data_line


def make_line_chart():
    data = get_line_data()
    return Line(data)
