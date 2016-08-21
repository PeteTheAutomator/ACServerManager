from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from .models import Preset
from .tasks import write_config, kick_services, get_server_status, stop_services
from time import sleep


def launch_preset(request, preset_id):
    preset = Preset.objects.get(id=preset_id)
    write_config(preset_id=preset.id)
    kick_services(preset_id=preset.id)

    #template = loader.get_template('launch_preset.html')
    #context = {'preset': preset}
    #return HttpResponse(template.render(context, request))

    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    sleep(2)
    get_server_status()
    sleep(3)
    return redirect('/admin/session/preset/')


def stop_preset(request, preset_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    stop_services(preset_id)
    sleep(2)
    get_server_status()
    sleep(3)
    return redirect('/admin/session/preset/')
