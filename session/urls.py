from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^preset/(?P<preset_id>[0-9]+)/launch/$', views.launch_preset, name='launch_preset'),
]