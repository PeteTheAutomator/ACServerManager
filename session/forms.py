from django import forms
from library.models import Track, TrackDynamism, Weather, Car
from session.models import Preset
from django.conf import settings


class EnvironmentForm(forms.Form):
    track = forms.ModelChoiceField(queryset=Track.objects.all())
    track_dynamism = forms.ModelChoiceField(queryset=TrackDynamism.objects.all())
    weather = forms.ModelChoiceField(queryset=Weather.objects.all())
    time_of_day = forms.ChoiceField(Preset.TIME_OF_DAY_CHOICES)


class EntrySetForm(forms.Form):
    car = forms.ModelChoiceField(queryset=Car.objects.all())
    quantity = forms.IntegerField()
    apply_fixed_setup = forms.BooleanField(required=False, help_text='If you have a fixed setup stored for this car, tick this box to apply it - otherwise allow racers to apply their own customisations in-game')


EntrySetFormSet = forms.formset_factory(EntrySetForm, extra=6)


class SessionTypeForm(forms.Form):
    practice_time = forms.IntegerField()
    qualify_time = forms.IntegerField()
    race_laps = forms.IntegerField()


class SettingsForm(forms.Form):
    name = forms.CharField(help_text='The name of the server - this will appear in the Assetto Corsa\'s listing of online servers for the public to join')
    welcome_message = forms.CharField(help_text='Place a welcome message here - this will display some dialog to clients upon joining a session which they must click to close', widget=forms.Textarea)
    admin_password = forms.CharField(help_text='Server Admin Password - joining the session using this password grants the user admin privilges (allowing you to skip sessions, kick users, etc)')
    minorating_grade = forms.ChoiceField(choices=settings.CONSTANCE_ADDITIONAL_FIELDS['mr_grade_choices'][1]['choices'])
    client_send_interval = forms.IntegerField(help_text='refresh rate of packet sending by the server. 10Hz = ~100ms. Higher number = higher MP quality = higher bandwidth resources needed. Really high values can create connection issues')
    minorating_server_trust_token = forms.CharField(help_text='this value is initialised when the server contacts Minorating for the first time; you may wish to record this value if migrating to another server')
