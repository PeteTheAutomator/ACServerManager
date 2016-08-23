from django.contrib import admin
from .models import Car, CarSkin, CarTag, Track, TrackDynamism, Weather, Document


class DocumentAdmin(admin.ModelAdmin):
    model = Document
    list_display = ('docfile', 'process_assets',)
    actions = None

    def process_assets(self, obj):
        return '<a href="/library/document/' + str(obj.pk) + '/process/">Process</a>'
    process_assets.allow_tags = True


admin.site.register(Car)
admin.site.register(CarSkin)
admin.site.register(CarTag)
admin.site.register(Track)
admin.site.register(TrackDynamism)
admin.site.register(Weather)
admin.site.register(Document, DocumentAdmin)
