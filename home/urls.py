from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from constance import config

from . import views

app_name = 'home'
urlpatterns = [
  # ex: /
  url(r'^$', views.get_index, name = 'index'),
  url(r'^photos/$', views.get_index_photos, name = 'index-photos'),
  url(r'^(?P<category>[\w-]+)/$', views.get_category, name = 'category'),
  url(r'^(?P<category>[\w-]+)/pages/$', views.get_category_pages, name = 'category-pages'),
  url(r'^(?P<category>[\w-]+)/(?P<page>[\w-]+)/$', views.get_category, name = 'page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)