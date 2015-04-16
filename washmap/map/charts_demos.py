from bokeh.charts import Line
from pandas import DataFrame
from stats.models import StatValue


def get_water_line_data():
    wat_stats = StatValue.objects.filter(description__code='WNTI_%')
    wat_stats = wat_stats.filter(country__name='South Africa')
    wat_stats = wat_stats.values('value', 'year')
    wat_data_line = DataFrame.from_records(
        wat_stats, coerce_float=True, index='year'
    )
    wat_data_line = wat_data_line[wat_data_line['value'] > 0]
    return wat_data_line


def make_line_chart():
    data = get_water_line_data()
    return Line(data)
