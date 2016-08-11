''' PARKING CUSTOM FORMS FOR NOW


from django import forms
from .models import Environment, EntryGroup, Entry


class EnvironmentForm(forms.ModelForm):
    class Meta:
        model = Environment
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(EnvironmentForm, self).__init__(*args, **kwargs)
        self.fields['voting_quorum'].widget.attrs.update({'class': 'advanced'})
        self.fields['vote_duration'].widget.attrs.update({'class': 'advanced'})


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ('',)


EntryFormSet = forms.formset_factory(EntryForm, extra=1)


class EntryGroupForm(forms.ModelForm):
    class Meta:
        model = EntryGroup
        exclude = ('',)
'''
