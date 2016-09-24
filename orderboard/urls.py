from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^move/([\d]*)/left$', views.move_left),
    url(r'^move/([\d]*)/right', views.move_right),
]
