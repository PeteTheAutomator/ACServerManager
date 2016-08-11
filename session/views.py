''' PARKING CUSTOM UI FOR NOW

from django.shortcuts import render, get_object_or_404, redirect
from .models import Environment, EntryGroup
from .forms import EnvironmentForm, EntryGroupForm, EntryForm, EntryFormSet


def list_environments(request):
    environment_list = Environment.objects.all()
    return render(request, 'environment_list.html', {'environment_list': environment_list})


def get_environment(request, environment_id):
    environment = get_object_or_404(Environment, pk=environment_id)
    entrygroups = environment.entrygroup_set.all()
    if request.method == 'POST':
        form = EnvironmentForm(request.POST, instance=environment)
        if form.is_valid():
            environment = form.save(commit=False)
            environment.save()
            return redirect('list_environments')
    else:
        form = EnvironmentForm(instance=environment)

    return render(request, 'environment_details.html', {'form': form, 'entrygroups': entrygroups})


def new_environment(request):
    if request.method == 'POST':
        form = EnvironmentForm(request.POST)
        if form.is_valid():
            environment = form.save(commit=False)
            environment.save()
            return redirect('list_environments')
    else:
        form = EnvironmentForm()
    return render(request, 'environment_details.html', {'form': form})


def new_entrygroup(request, environment_id):
    if request.method == 'POST':
        form = EntryGroupForm(request.POST)
        if form.is_valid():
            entrygroup = form.save(commit=False)
            entrygroup.save()
            return redirect('list_environments')
    else:
        form = EntryGroupForm()
        entry_formset = EntryFormSet()
    return render(request, 'entrygroup_details.html', {'form': form, 'entry_formset': entry_formset})


def edit_entrygroup(request, environment_id, entrygroup_id):
    entrygroup = get_object_or_404(EntryGroup, pk=entrygroup_id)
    if request.method == 'POST':
        form = EntryGroupForm(request.POST, instance=entrygroup)
        if form.is_valid():
            entrygroup = form.save(commit=False)
            entrygroup.save()
            return redirect('list_environments')
    else:
        form = EntryGroupForm(instance=entrygroup)
        entries = entrygroup.entry_set.all()
        entry_list = []
        for entry in entries:
            entry_list.append(
                {
                    'driver_preset': entry.driver_preset,
                    'name': entry.name,
                    'car': entry.car,
                    'spectator_mode': entry.spectator_mode,
                    'team': entry.team,
                    'guid': entry.guid,
                    'ballast': entry.ballast,
                }
            )

        entry_formset = EntryFormSet(initial=entry_list)
    return render(request, 'entrygroup_details.html', {'form': form, 'entry_formset': entry_formset})

'''
