"""acserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from session.views import launch_preset, stop_preset, upgrade
from library.views import process_assetcollection

admin.site.site_header = 'Assetto Corsa Server Manager'
admin.site.site_title = 'Assetto Corsa Server Manager'

urlpatterns = [
    url(r'^admin/session/preset/(?P<preset_id>[0-9]+)/launch/$', launch_preset, name='launch_preset'),
    url(r'^admin/session/preset/(?P<preset_id>[0-9]+)/stop/$', stop_preset, name='stop_preset'),
    url(r'^admin/upgrade/', upgrade, name='upgrade'),
    url(r'^admin/library/assetcollection/(?P<assetcollection_id>[0-9]+)/process/$', process_assetcollection, name='process_assetcollection'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
]
