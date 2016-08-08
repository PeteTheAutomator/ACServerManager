from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^preset/$', views.index),
    url(r'^preset/(?P<preset_id>[0-9]+)/$', views.detail, name='detail')
]