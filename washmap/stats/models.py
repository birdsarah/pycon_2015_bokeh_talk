from __future__ import absolute_import, unicode_literals
from django.db import models

from country.models import Country

from adminsortable.fields import SortableForeignKey
from adminsortable.models import Sortable


class StatDescription(Sortable):
    class Meta(Sortable.Meta):
        pass

    description = models.TextField()
    code = models.SlugField()

    def __unicode__(self):
        return self.description


class StatValue(models.Model):
    class Meta:
        unique_together = ('description', 'country', 'year')

    description = models.ForeignKey(StatDescription)
    country = models.ForeignKey(Country)
    year = models.IntegerField()
    value = models.DecimalField(max_digits=20, decimal_places=10, null=True, blank=True)  # nopep8

    def __unicode__(self):
        return "%s, %s, %s" % (
            self.country,
            self.year,
            self.value
        )
