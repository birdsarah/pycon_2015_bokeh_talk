from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import LineView

urlpatterns = patterns('',
    url(r'line_view', LineView.as_view()),
)
