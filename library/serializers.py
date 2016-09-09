from .models import Car, CarSkin, CarTag, Track, TrackDynamism, Weather, AssetCollection
from rest_framework import serializers


class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car


class CarSkinSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarSkin


class CarTagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CarTag


class TrackSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Track


class TrackDynamismSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrackDynamism


class WeatherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Weather


class AssetCollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AssetCollection

