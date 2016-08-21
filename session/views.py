from django.http import HttpResponse
from django.template import loader
from .models import Preset
from .tasks import write_config, kick_services, get_server_status


def launch_preset(request, preset_id):
    preset = Preset.objects.get(id=preset_id)
    write_config(preset_id=preset.id)
    kick_services(preset_id=preset.id)
    get_server_status()

    template = loader.get_template('launch_preset.html')
    context = {'preset': preset}
    return HttpResponse(template.render(context, request))
