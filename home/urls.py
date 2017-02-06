from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from constance import config

from . import views

app_name = 'home'
urlpatterns = [
  # ex: /
  url(r'^$', views.index, name = 'index'),
  url(r'^(?P<category>[\w-]+)/$', views.category, name = 'category'),
  url(r'^(?P<category>[\w-]+)/(?P<page>[\w-]+)/$', views.category, name = 'page'),
]