from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^environment/$', views.list_environments, name='list_environments'),
    url(r'^environment/(?P<environment_id>[0-9]+)/$', views.get_environment, name='get_environment'),
    url(r'^environment/new/$', views.new_environment, name='new_environment'),
    url(r'^environment/(?P<environment_id>[0-9]+)/entrygroup/new/$', views.new_entrygroup, name='new_entrygroup'),
    url(r'^environment/(?P<environment_id>[0-9]+)/entrygroup/(?P<entrygroup_id>[0-9]+)/$', views.edit_entrygroup,
        name='edit_entrygroup'),
]