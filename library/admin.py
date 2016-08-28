from django.contrib import admin
from .models import Car, CarSkin, CarTag, Track, TrackDynamism, Weather, AssetCollection
from background_task.models import Task, CompletedTask
from django.conf import settings


class AssetCollectionAdmin(admin.ModelAdmin):
    model = AssetCollection
    list_display = ('collection', 'process_assets',)
    actions = None

    def process_assets(self, obj):
        return '<a href="/admin/library/assetcollection/' + str(obj.pk) + '/process/">Process</a>'
    process_assets.allow_tags = True


class CarAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    model = Car
    fields = ('brand', 'name', 'fixed_setup')
    readonly_fields = ('name', 'brand')
    actions = None


if settings.ACSERVER_FULL_ADMIN_VIEW:
    admin.site.register(Car, CarAdmin)
    admin.site.register(CarSkin)
    admin.site.register(CarTag)
    admin.site.register(Track)
    admin.site.register(TrackDynamism)
    admin.site.register(Weather)
    admin.site.register(AssetCollection, AssetCollectionAdmin)
else:
    admin.site.register(Car, CarAdmin)
    admin.site.register(AssetCollection, AssetCollectionAdmin)
    admin.site.unregister(Task)
    admin.site.unregister(CompletedTask)
