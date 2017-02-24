from django.conf.urls import url

from . import views

app_name = 'travel'
urlpatterns = [
  # ex: /travel/
  url(r'^$', views.index, name = 'index'),
  # ex: /travel/location/
  url(r'^location/$', views.location, name = 'location'),
  url(r'^places/$', views.places, name = 'places'),
  url(r'^world/$', views.world, name = 'world')
]