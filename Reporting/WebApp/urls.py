from django.conf.urls import patterns, url

from WebApp import views

urlpatterns = patterns('',
  url(r'^$', views.upload, name='upload'),
  url(r'^confirm/$', views.confirm, name='confirm'),
)