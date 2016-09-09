from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Car, CarSkin, CarTag, Track, TrackDynamism, Weather, AssetCollection
from .serializers import CarSerializer, CarSkinSerializer, CarTagSerializer, TrackSerializer, TrackDynamismSerializer, \
    WeatherSerializer, AssetCollectionSerializer
from .tasks import process_assets


@login_required
def process_assetcollection(request, assetcollection_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    process_assets(assetcollection_id)
    return redirect('/admin/library/assetcollection/')


class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Cars to be viewed or edited.
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarSkinViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CarSkins to be viewed or edited.
    """
    queryset = CarSkin.objects.all()
    serializer_class = CarSkinSerializer


class CarTagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CarTags to be viewed or edited.
    """
    queryset = CarTag.objects.all()
    serializer_class = CarTagSerializer


class TrackViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Tracks to be viewed or edited.
    """
    queryset = Track.objects.all()
    serializer_class = TrackSerializer


class TrackDynamismViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TrackDynamisms to be viewed or edited.
    """
    queryset = TrackDynamism.objects.all()
    serializer_class = TrackDynamismSerializer


class WeatherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Weathers to be viewed or edited.
    """
    queryset = Weather.objects.all()
    serializer_class = Weather


class AssetCollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AssetCollections to be viewed or edited.
    """
    queryset = AssetCollection.objects.all()
    serializer_class = AssetCollectionSerializer
