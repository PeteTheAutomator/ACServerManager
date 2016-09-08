from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .tasks import write_config, kick_services, get_server_status, stop_services, perform_upgrade
from time import sleep

from session.models import Entry, Preset
from library.models import CarSkin, Weather, TrackDynamism, Track
from formtools.wizard.views import SessionWizardView
from session.forms import EnvironmentForm, SessionTypeForm, EntrySetFormSet, SettingsForm

from django.views import generic

from constance import config as constance_config


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
    form_data = [form.cleaned_data for form in form_list]

    p = Preset(
        track=form_data[0]['track'],
        track_dynamism=form_data[0]['track_dynamism'],
        time_of_day=form_data[0]['time_of_day'],
        practice_time=form_data[2]['practice_time'],
        qualify_time=form_data[2]['qualify_time'],
        race_laps=form_data[2]['race_laps'],
    )
    p.save()
    p.weathers.add(form_data[0]['weather'])
    p.save()

    for entry_group in form_data[1]:
        if len(entry_group) == 0:
            continue

        car_skins = CarSkin.objects.filter(car=entry_group['car'])
        entry_count = 0
        car_skin_id = 0

        while entry_count < entry_group['quantity']:
            car_skin = car_skins[car_skin_id]
            e = Entry(
                preset=p,
                car=entry_group['car'],
                skin=car_skin,
                fixed_setup=entry_group['apply_fixed_setup']
            )
            e.save()

            if car_skin_id == (len(car_skins) - 1):
                car_skin_id = 0
            else:
                car_skin_id += 1

            entry_count += 1


FORMS = [
    ('environment', EnvironmentForm),
    ('entryset', EntrySetFormSet),
    ('session', SessionTypeForm),
]

TEMPLATES = {
    'environment': 'ac/entry_wizard.html',
    'entryset': 'ac/entry_wizard.html',
    'session': 'ac/entry_wizard.html',
}


class PresetWizard(SessionWizardView):
    form_list = FORMS

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    # Here we set default values for each of the wizard's steps (initial_dict_preliminary).  This
    # forms the wizard's "initial_dict" property which can evolve as steps progress based on
    # previous step data - e.g. a track's pitboxes influences the default value for car quantity.
    try:
        track_dynamism = TrackDynamism.objects.get(name='Fast')
    except TrackDynamism.DoesNotExist:
        track_dynamism = None

    try:
        weather = Weather.objects.get(name='Clear')
    except Weather.DoesNotExist:
        weather = None

    initial_dict_preliminary = {
        'environment': {
            'time_of_day': '11:00:00',
            'weather': weather,
            'track_dynamism': track_dynamism,
        },
        'session': {
            'practice_time': 0,
            'qualify_time': 12,
            'race_laps': 6,
        }
    }

    def get_form_initial(self, step):
        """
        Evolve the initial_dict for a step based on choices made in the previous step(s)
        :param step:
        :return: initial_dict
        """
        initial_dict_current = self.initial_dict_preliminary.get(step)
        if step == 'entryset':
            prev_data = self.storage.get_step_data('environment')
            track_id = prev_data.get('environment-track', '')
            try:
                pitboxes = Track.objects.get(id=track_id).pitboxes
                initial_dict_current['quantity'] = pitboxes
            except:
                pass
        return initial_dict_current

    def get_context_data(self, form, **kwargs):
        context = super(PresetWizard, self).get_context_data(form=form, **kwargs)
        if self.steps.current == 'entryset':
            track_info = {
                'name': None,
                'pitboxes': None,
            }
            prev_data = self.storage.get_step_data('environment')
            track_id = prev_data.get('environment-track', '')
            try:
                track = Track.objects.get(id=track_id)
                track_info['name'] = track.name
                track_info['pitboxes'] = track.pitboxes
            except Track.DoesNotExist:
                pass
            context.update({'track_info': track_info})
        return context

    def done(self, form_list, **kwargs):
        process_form_data(form_list)
        return HttpResponseRedirect('/ac/preset/')


def constance_config_view(request):
    initial_dict = {
        'name': constance_config.name,
        'welcome_message': constance_config.welcome_message,
        'admin_password': constance_config.admin_password,
        'minorating_grade': constance_config.minorating_grade,
        'minorating_server_trust_token': constance_config.minorating_server_trust_token,
        'client_send_interval': constance_config.client_send_interval,
    }

    if request.method == 'POST':
        form = SettingsForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            constance_config.name = form_data['name']
            constance_config.welcome_message = form_data['welcome_message']
            constance_config.admin_password = form_data['admin_password']
            constance_config.minorating_grade = form_data['minorating_grade']
            constance_config.minorating_server_trust_token = form_data['minorating_server_trust_token']
            constance_config.client_send_interval = form_data['client_send_interval']
            return HttpResponseRedirect('/ac/')
    else:
        form = SettingsForm(initial=initial_dict)

    return render(request, 'ac/settings.html', {'form': form})


def main_menu(request):
    return render(request, 'ac/menu.html')


class PresetIndexView(generic.ListView):
    template_name = 'ac/list.html'
    context_object_name = 'preset_list'

    def get_queryset(self):
        return Preset.objects.all()


PRESET_FIELDS = ('name', 'track', 'track_dynamism', 'max_clients', 'pickup_mode_enabled', 'session_password',
                 'practice_time', 'practice_is_open', 'qualify_time', 'qualify_is_open', 'race_laps', 'race_wait_time',
                 'race_is_open', 'weathers', 'time_of_day', 'tc_allowed', 'abs_allowed', 'stability_allowed',
                 'autoclutch_allowed', 'force_virtual_mirror', 'damage_multiplier', 'fuel_rate',
                 'tyre_blankets_allowed', 'tyre_wear_rate', 'allowed_tyres_out', 'voting_quorum', 'vote_duration',
                 'kick_quorum', 'race_over_time', 'loop_mode', 'blacklist_mode', 'qualify_max_wait_perc', 'start_rule')


class PresetUpdate(generic.UpdateView):
    model = Preset
    template_name = 'ac/detail.html'
    fields = PRESET_FIELDS
    success_url = '/ac/preset/'

class PresetDelete(generic.DeleteView):
    model = Preset
    success_url = '/ac/preset/'