from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Preset
from .tasks import write_config, kick_services, get_server_status, stop_services, perform_upgrade
from time import sleep


@login_required
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


@login_required
def stop_preset(request, preset_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    stop_services(preset_id)
    sleep(2)
    get_server_status()
    sleep(3)
    return redirect('/admin/session/preset/')


@login_required
def upgrade(request):
    perform_upgrade()
