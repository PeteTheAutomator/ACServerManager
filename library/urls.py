from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^assetcollection/(?P<assetcollection_id>[0-9]+)/process/$', views.process_assetcollection, name='process_assetcollection'),
]