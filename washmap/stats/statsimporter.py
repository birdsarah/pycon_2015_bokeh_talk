from __future__ import absolute_import, unicode_literals

from copy import deepcopy

from django.core.exceptions import ValidationError
from django.utils.datastructures import SortedDict

from decimal import Decimal

from import_export.fields import Field
from import_export.instance_loaders import ModelInstanceLoader
from import_export.resources import ModelResource
from import_export.widgets import DecimalWidget

from country.models import Country
from .models import StatValue


# as defined in https://docs.python.org/2/library/decimal.html#decimal-faq
def remove_exponent(d):
    '''Remove exponent and trailing zeros.

    >>> remove_exponent(Decimal('5E+3'))
    Decimal('5000')

    '''
    return d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()


class CountryField(Field):

    def get_value(self, obj):
        country = obj.get_country()
        if country:
            return country.name
        return None


class YearField(Field):
    def __init__(self, year, column_name=None, widget=None, readonly=False):

        attribute = 'placeholder'
        # attribute = 'year-%d' % year
        # We want this field to be imported by Resource.import_obj()

        if widget is None:
            widget = DecimalWidget()

        super(YearField, self).__init__(attribute, column_name, widget, readonly)  # nopep8
        self.attribute = 'year-%d' % year
        self.year = year

    def clean(self, data):
        # Interpret NA values as StatValue.value == None
        if data[self.column_name] == '':
            return False

        if data[self.column_name] == 'NA':
            return None

        try:
            cleaned_data = super(YearField, self).clean(data)
        except Decimal.InvalidOperation as e:
            raise ValidationError(
                "'%s': value is not a valid decimal: '%s'"
                % (self.column_name, data[self.column_name])
            )
        except Exception as e:
            raise ValidationError("'%s': %s" % (self.column_name, e))

        return cleaned_data

    def save(self, obj, data):
        if not self.readonly:
            # value can be a Decimal, None or False
            value = self.clean(data)
            if value is not False:  # skip adding if False
                obj.add_yearfield(self.year, value)

    def get_value(self, obj):
        return obj.get_value(self.year)

    def export(self, obj):
        value = self.get_value(obj)
        if value is None:
            return "NA"
        if value is False:
            return ""
        display_value = remove_exponent(value)
        return self.widget.render(display_value)


class StatValueRowInstance(object):
    """
    Maps an import row onto a collection of StatValue objects.

    Values for 'statistic' (StatDescription) and 'country' are initialized
    with the instance loader (called per row).

    YearFields are added for each non-country column.

    Implements ORM like interface on row:
        .save
        .delete

    """
    years = None
    pk = None  # Has to be faked to keep import-export happy

    def __init__(self, statistic, country):
        self.statistic = statistic
        self.country = country

        self.years = SortedDict()
        self.load_statvalues()

    def get_country(self):
        return self.country

    def load_statvalues(self):
        values = StatValue.objects.filter(description=self.statistic,
                                          country=self.country)
        to_update = SortedDict(values.values_list('year', 'value'))
        self.years.update(to_update)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def add_yearfield(self, year, value):
        self.years[year] = value

    def get_value(self, year):
        """ Return StatValue.value for year:
            Decimal (has value)
            None    (if value is None) (NA)
            False   (if key (year) doesn't exist)
        """
        return self.years.get(year, False)

    def save(self):
        for year, value in self.years.items():
            try:
                obj = StatValue.objects.get(
                    description=self.statistic,
                    country=self.country,
                    year=year
                )
                obj.value = value
            except StatValue.DoesNotExist:
                obj = StatValue(
                    description=self.statistic,
                    country=self.country,
                    year=year,
                    value=value)

            obj.save()


class StatValueInstanceLoader(ModelInstanceLoader):

    def __init__(self, resource, dataset=None):
        self.resource = resource
        self.dataset = dataset

    def get_queryset(self):
        return self.resource._meta.model.objects.all()

    def get_instance(self, row):

        try:
            country_field = self.resource.fields['country']
            country_name = country_field.clean(row)
            country = Country.objects.get(name=country_name)
        except Country.DoesNotExist:
            raise AttributeError("Country %s does not exist" % country_name)

        return StatValueRowInstance(self.resource.statistic, country)


class StatisticResource(ModelResource):
    """
        StatDescription

        StatValue
            Year
            @Country
            @StatDescription

        Stat Description
        Country | Year | Year | Year ... |
        A..     |
        B..     |

    """

    class Meta:
        model = None  # see StatValueRowInstance instead
        fields = ()
        instance_loader_class = StatValueInstanceLoader
        import_id_fields = ['country']

    country = CountryField(attribute='name', readonly=True)

    def __init__(self, statistic, *args, **kwargs):
        self.statistic = statistic
        super(StatisticResource, self).__init__(*args, **kwargs)

    def before_import(self, dataset, real_dry_run):
        # Presume first column is country column
        year_headers = dataset.headers[1:]

        # check they are valid, unique, etc

        for year_header in year_headers:
            year = int(year_header)
            self.fields['year-%d' % year] = YearField(year, column_name='%s' % year)  # nopep8

    def get_dynamic_fields(self):
        year_fields = SortedDict()

        values_qs = StatValue.objects.filter(description=self.statistic)
        years = values_qs.values_list('year', flat=True).distinct()

        for year in sorted(years):
            year_fields['year-%d' % year] = YearField(year, column_name='%s' % year)  # nopep8

        return year_fields

    def get_queryset(self):
        countries = Country.objects.all().order_by('name')
        statvalues = []
        for country in countries:
            inst = StatValueRowInstance(self.statistic, country)
            statvalues.append(inst)

        class dummy_queryset(object):
            def iterator(self):
                return statvalues

        return dummy_queryset()
