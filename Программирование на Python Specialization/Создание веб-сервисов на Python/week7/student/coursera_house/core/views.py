from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import JsonResponse

from .models import Setting
from .form import ControllerForm
from .tasks import poll_controller


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
        context['data'] = {}
        return context

    def get_initial(self):
        return {}

    def form_valid(self, form):
        bedroom_target_temperature_value = form.cleaned_data['bedroom_target_temperature']
        hot_water_target_temperature_value = form.cleaned_data['hot_water_target_temperature']
        bedroom_light_value = form.cleaned_data['bedroom_light']
        bathroom_light_value = form.cleaned_data['bathroom_light']

        get_or_update(
            'bedroom_target_temperature',
            'Bedroom target temperature',
            bedroom_target_temperature_value
        )
        get_or_update(
            'hot_water_target_temperature',
            'Hot water target temperature value',
            hot_water_target_temperature_value
        )
        get_or_update(
            'bedroom_light',
            'Bedroom light',
            bedroom_light_value
        )
        get_or_update(
            'bathroom_light',
            'Bathroom light',
            bathroom_light_value
        )
        ss = Setting.objects.all()
        return super(ControllerView, self).get(form)


def controller_data(request):
    current_controller_data = poll_controller()
    data = {'data': current_controller_data}
    return JsonResponse(data)
