from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from constance import config

from . import views

app_name = 'home'
urlpatterns = [
  # ex: /
  url(r'^$', views.get_index, name = 'index'),
  url(r'^(?P<category>[\w-]+)/$', views.get_category, name = 'category'),
  url(r'^(?P<category>[\w-]+)/(?P<page>[\w-]+)/$', views.get_category, name = 'page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)