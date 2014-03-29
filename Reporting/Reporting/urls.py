from django.conf.urls import patterns, include, url
from django.contrib import admin
from WebApp import views as webAppViews
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Reporting.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^upload', webAppViews.upload),
)
