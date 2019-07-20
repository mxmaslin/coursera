import requests
from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import Setting
from .form import ControllerForm



def get_or_update(controller_name, label, value):
    try:
        entry = Setting.objects.get(controller_name=controller_name)
    except Setting.DoesNotExist:
        Setting.objects.create(
            controller_name=controller_name,
            label=label,
            value=value
        )
    else:
        entry.value = value
        entry.save()


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        headers = {'Authorization': f'Bearer {settings.SMART_HOME_ACCESS_TOKEN}'}
        current_controller_data = requests.get(
            settings.SMART_HOME_API_URL, headers=headers
        ).json()
        context['data'] = current_controller_data
        return context

    def get_initial(self):
        initial = super(ControllerView, self).get_initial()
        initial['bedroom_target_temperature'] = 21
        initial['hot_water_target_temperature'] = 80
        return initial

    def form_valid(self, form):
        get_or_update(
            'bedroom_target_temperature',
            'Bedroom target temperature',
            form.cleaned_data['bedroom_target_temperature']
        )
        get_or_update(
            'hot_water_target_temperature',
            'Hot water target temperature value',
            form.cleaned_data['hot_water_target_temperature']
        )
        get_or_update(
            'bedroom_light',
            'Bedroom light',
            form.cleaned_data['bedroom_light']
        )
        get_or_update(
            'bathroom_light',
            'Bathroom light',
            form.cleaned_data['bathroom_light']
        )
        return super(ControllerView, self).get(form)
