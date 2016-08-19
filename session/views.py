from django.http import HttpResponse
from django.template import loader
from .models import Preset


def launch_preset(request, preset_id):
    preset = Preset.objects.get(id=preset_id)
    template = loader.get_template('launch_preset.html')
    context = {'preset': preset}
    return HttpResponse(template.render(context, request))
