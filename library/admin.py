from django.contrib import admin
from .models import Car, CarSkin, CarTag, Track, TrackDynamism, Weather


admin.site.register(Car)
admin.site.register(CarSkin)
admin.site.register(CarTag)
admin.site.register(Track)
admin.site.register(TrackDynamism)
admin.site.register(Weather)
