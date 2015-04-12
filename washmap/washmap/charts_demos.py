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


def get_line_data(country_name):
    wat_stats = StatValue.objects.filter(description__code='WNTI_%')
    wat_stats = wat_stats.filter(country__name=country_name)
    wat_stats = wat_stats.values('value', 'year')
    wat_stats_df = DataFrame.from_records(
        wat_stats, coerce_float=True,
    )
    wat_stats_df['wat_value'] = wat_stats_df['value']

    san_stats = StatValue.objects.filter(description__code='SNTI_%')
    san_stats = san_stats.filter(country__name=country_name)
    san_stats = san_stats.values('value', 'year')
    san_stats_df = DataFrame.from_records(
        san_stats, coerce_float=True,
    )
    san_stats_df['san_value'] = san_stats_df['value']

    wat_san = wat_stats_df.merge(san_stats_df, on='year')
    return wat_san
