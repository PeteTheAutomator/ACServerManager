from django.contrib import admin

from .models import Car, Track, TrackDynamism, Weather, ServerSetting


admin.site.register(Car)
admin.site.register(Track)
admin.site.register(TrackDynamism)
admin.site.register(Weather)
admin.site.register(ServerSetting)
