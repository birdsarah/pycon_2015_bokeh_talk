from django.conf.urls import patterns, include, url
from django.contrib import admin
from adminplus.sites import AdminSitePlus

admin.site = AdminSitePlus()
admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('washmap.washmap.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
