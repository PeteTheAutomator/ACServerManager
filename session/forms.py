from django import forms
from library.models import Track, TrackDynamism, Weather, Car
from session.models import Preset, ServerSetting


class EnvironmentForm(forms.Form):
    server_setting = forms.ModelChoiceField(queryset=ServerSetting.objects.all())
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

