from __future__ import unicode_literals, absolute_import

from django.conf.urls import patterns, url

from .views import (
    WashMapServerView,
    LineStaticView,
    WashMapStaticMapView,
    WashMapStaticMapToolsView,
    WashMapStaticMapToolsLinkedView,
    WashMapStaticMapToolsLinkedTabbedView,
    WashMapStaticAllView,
)

urlpatterns = patterns('',
    url(r'^$', WashMapServerView.as_view()),
    url(r'^line$', LineStaticView.as_view()),
    url(r'^static_map$', WashMapStaticMapView.as_view()),
    url(r'^static_map_tools$', WashMapStaticMapToolsView.as_view()),
    url(r'^static_map_tools_linked$', WashMapStaticMapToolsLinkedView.as_view()),
    url(r'^static_map_tools_linked_tabbed$', WashMapStaticMapToolsLinkedTabbedView.as_view()),
    url(r'^static_all$', WashMapStaticAllView.as_view()),
)
