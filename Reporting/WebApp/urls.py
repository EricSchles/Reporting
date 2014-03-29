from django.conf.urls import patterns, url

from WebApp import views

urlpatterns = patterns('',
  url(r'^upload/$', views.upload, name='upload'),
  url(r'^upload/confirm/$', views.confirm, name='confirm'),
  url(r'^upload/submit/$', views.success, name='Success'),
  url(r'^websites/(?P<website_id>[0-9]+)/?$', views.website_ads, name='Website Ads'),
  url(r'^websites/$', views.websites, name='Websites'),
)
