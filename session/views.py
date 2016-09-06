from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .tasks import write_config, kick_services, get_server_status, stop_services, perform_upgrade
from time import sleep

from session.models import Entry, Preset, ServerSetting
from library.models import CarSkin, Weather, TrackDynamism, Track
from formtools.wizard.views import SessionWizardView
from session.forms import EntrySetForm, EnvironmentForm, SessionTypeForm



@login_required
def launch_preset(request, preset_id):
    preset = Preset.objects.get(id=preset_id)
    write_config(preset_id=preset.id)
    kick_services(preset_id=preset.id)

    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    sleep(5)
    get_server_status()
    sleep(3)
    return redirect('/admin/session/preset/')


@login_required
def stop_preset(request, preset_id):
    # TODO: make it pretty (yeah - it's horrible, but let's get something vaguely working)
    stop_services(preset_id)
    sleep(5)
    get_server_status()
    sleep(3)
    return redirect('/admin/session/preset/')


@login_required
def upgrade(request):
    perform_upgrade()
    return redirect('/admin/')


def process_form_data(form_list):
    form_data_list = [form.cleaned_data for form in form_list]
    form_data = {}
    for d in form_data_list:
        form_data.update(d)

    # TODO: add weather to many-to-many
    p = Preset(
        server_setting=form_data['server_setting'],
        track=form_data['track'],
        track_dynamism=form_data['track_dynamism'],
        time_of_day=form_data['time_of_day'],
        practice_time=form_data['practice_time'],
        qualify_time=form_data['qualify_time'],
        race_laps=form_data['race_laps'],
    )
    p.save()
    p.weathers.add(form_data['weather'])
    p.save()

    car_skins = CarSkin.objects.filter(car=form_data['car'])
    entry_count = 0
    car_skin_id = 0
    while entry_count < form_data['quantity']:
        car_skin = car_skins[car_skin_id]
        e = Entry(
            preset=p,
            car=form_data['car'],
            skin=car_skin,
            fixed_setup=form_data['apply_fixed_setup']
        )
        e.save()

        if car_skin_id == (len(car_skins) - 1):
            car_skin_id = 0
        else:
            car_skin_id += 1

        entry_count += 1


class PresetWizard(SessionWizardView):
    form_list = [EnvironmentForm, EntrySetForm, SessionTypeForm]
    template_name = 'admin/session/preset/presetwizard.html'

    # Here we set default values for each of the wizard's steps (initial_dict_preliminary).  This
    # forms the wizard's "initial_dict" property which can evolve as steps progress based on
    # previous step data - e.g. a track's pitboxes influences the default value for car quantity.
    all_server_settings = ServerSetting.objects.all()
    if len(all_server_settings) > 0:
        static_server_setting = all_server_settings[0]
    else:
        static_server_setting = None

    try:
        track_dynamism = TrackDynamism.objects.get(name='Fast')
    except TrackDynamism.DoesNotExist:
        track_dynamism = None

    try:
        weather = Weather.objects.get(name='Clear')
    except Weather.DoesNotExist:
        weather = None

    initial_dict_preliminary = {
        '0': {
            'server_setting': static_server_setting,
            'time_of_day': '11:00:00',
            'weather': weather,
            'track_dynamism': track_dynamism,
        },
        '1': {
            'quantity': None,
        },
        '2': {
            'practice_time': 0,
            'qualify_time': 12,
            'race_laps': 6,
        }
    }

    def get_form_initial(self, step):
        '''
        Evolve the initial_dict for a step based on choices made in the previous step(s)
        :param step:
        :return: initial_dict
        '''
        initial_dict_current = self.initial_dict_preliminary.get(step)
        if step == '1':
            prev_data = self.storage.get_step_data('0')
            track_id = prev_data.get('0-track', '')
            try:
                pitboxes = Track.objects.get(id=track_id).pitboxes
                initial_dict_current['quantity'] = pitboxes
            except:
                pass
        return initial_dict_current

    def done(self, form_list, **kwargs):
        process_form_data(form_list)
        return HttpResponseRedirect('/admin/session/preset/')
