from django.contrib import admin
from .models import Car, CarSkin, CarTag, Track, TrackDynamism, Weather, AssetCollection
from background_task.models import Task, CompletedTask
from django.conf import settings


class DocumentAdmin(admin.ModelAdmin):
    model = AssetCollection
    list_display = ('collection', 'process_assets',)
    actions = None

    def process_assets(self, obj):
        return '<a href="/library/assetcollection/' + str(obj.pk) + '/process/">Process</a>'
    process_assets.allow_tags = True


if settings.ACSERVER_FULL_ADMIN_VIEW:
    admin.site.register(Car)
    admin.site.register(CarSkin)
    admin.site.register(CarTag)
    admin.site.register(Track)
    admin.site.register(TrackDynamism)
    admin.site.register(Weather)
    admin.site.register(AssetCollection, DocumentAdmin)
else:
    admin.site.register(AssetCollection, DocumentAdmin)
    admin.site.unregister(Task)
    admin.site.unregister(CompletedTask)
