from django.conf.urls import url

from . import views

app_name = 'index'
urlpatterns = [
    # ex: /
    url(r'^$', views.index, name = 'index'),
]