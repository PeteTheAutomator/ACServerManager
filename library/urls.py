from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^document/(?P<document_id>[0-9]+)/process/$', views.process_document, name='process_document'),
]