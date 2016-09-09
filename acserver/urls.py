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
from rest_framework import routers
from session.views import PresetViewSet, EntryViewSet, launch_preset, stop_preset, upgrade, constance_config_view, PresetWizard, main_menu, \
    PresetIndexView, PresetAdd, PresetUpdate, PresetDelete
from library.views import process_assetcollection, CarViewSet, CarSkinViewSet, CarTagViewSet, TrackViewSet, \
    TrackDynamismViewSet, WeatherViewSet, AssetCollectionViewSet


admin.site.site_header = 'Assetto Corsa Server Manager'
admin.site.site_title = 'Assetto Corsa Server Manager'


router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)
router.register(r'carskins', CarSkinViewSet)
router.register(r'cartags', CarTagViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'trackdynamisms', TrackDynamismViewSet)
router.register(r'weathers', WeatherViewSet)
router.register(r'assetcollections', AssetCollectionViewSet)
router.register(r'presets', PresetViewSet)
router.register(r'entries', EntryViewSet)


urlpatterns = [
    url(r'^admin/session/preset/(?P<preset_id>[0-9]+)/launch/$', launch_preset, name='launch_preset'),
    url(r'^admin/session/preset/(?P<preset_id>[0-9]+)/stop/$', stop_preset, name='stop_preset'),
    url(r'^admin/session/presetwizard/', PresetWizard.as_view(), name='preset'),
    url(r'^admin/upgrade/', upgrade, name='upgrade'),
    url(r'^admin/library/assetcollection/(?P<assetcollection_id>[0-9]+)/process/$', process_assetcollection, name='process_assetcollection'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^chaining/', include('smart_selects.urls')),
#    url(r'^api/', include(router.urls)),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^ac/$', main_menu, name='main_menu'),
    url(r'^ac/settings/', constance_config_view, name='constance_config_view'),
    url(r'^ac/preset/$', PresetIndexView.as_view()),
    url(r'^ac/preset/add/$', PresetAdd.as_view(), name='preset-add'),
    url(r'^ac/preset/(?P<pk>[0-9])+/$', PresetUpdate.as_view(), name='preset-update'),
    url(r'^ac/preset/(?P<pk>[0-9])+/delete/$', PresetDelete.as_view(), name='preset-delete'),
    url(r'^ac/presetwizard/$', PresetWizard.as_view()),
]
