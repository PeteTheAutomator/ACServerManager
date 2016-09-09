from rest_framework import serializers
from .models import Preset, Entry


class PresetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Preset


class EntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entry
