from django.shortcuts import render, get_object_or_404
from .models import Preset
from library.models import Track

def index(request):
    preset_list = Preset.objects.all()
    context = {'preset_list': preset_list}
    return render(request, 'presets/index.html', context)


def detail(request, preset_id):
    preset = get_object_or_404(Preset, pk=preset_id)
    tracks = Track.objects.all()
    return render(request, 'presets/detail.html', {'preset': preset, 'tracks': tracks})
