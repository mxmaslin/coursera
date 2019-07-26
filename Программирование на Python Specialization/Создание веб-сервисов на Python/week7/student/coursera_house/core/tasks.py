from __future__ import absolute_import, unicode_literals
import requests
from celery import task
from django.conf import settings
from django.core.mail import EmailMessage
from .models import Setting


TOKEN = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {TOKEN}'}


@task()
def smart_home_manager():
    controller_data = requests.get(url, headers=headers).json().get('data')
    controller_data = {x['name']: x for x in controller_data}
    payload = {
        'controllers': []
    }

    water_leaks = controller_data['leak_detector']['value']
    if water_leaks:
        payload['controllers'].append({'name': 'cold_water', 'value': False})
        payload['controllers'].append({'name': 'hot_water', 'value': False})
        email = EmailMessage(
            'Subject',
            'Message.',
            settings.EMAIL_HOST,
            [settings.EMAIL_RECEPIENT],
        )
        email.send(fail_silently=False)

    cold_water_on = controller_data['cold_water']['value']
    if not cold_water_on:
        payload['controllers'].append({'name': 'boiler', 'value': False})
        payload['controllers'].append({'name': 'washing_machine', 'value': "off"})

    boiler_temperature = controller_data['boiler_temperature']['value']
    hot_water_target_temperature = Setting.objects.get(
        controller_name='hot_water_target_temperature').value
    hot_water_low_temp = hot_water_target_temperature - hot_water_target_temperature * 0.1
    hot_water_ok_temp = hot_water_target_temperature + hot_water_target_temperature * 0.1

    bedroom_temperature = controller_data['bedroom_temperature']['value']
    bedroom_target_temperature = Setting.objects.get(
        controller_name='bedroom_target_temperature').value
    bedroom_low_temp = bedroom_target_temperature - bedroom_target_temperature * 0.1
    bedroom_high_temp = bedroom_target_temperature + bedroom_target_temperature * 0.1

    smoke_detector = controller_data['smoke_detector']['value']

    if smoke_detector:
        payload['controllers'].append({'name': 'air_conditioner', 'value': False})
        payload['controllers'].append({'name': 'bathroom_light', 'value': False})
        payload['controllers'].append({'name': 'bedroom_light', 'value': False})
        payload['controllers'].append({'name': 'boiler', 'value': False})
        payload['controllers'].append({'name': 'washing_machine', 'value': False})
    else:
        if boiler_temperature < hot_water_low_temp:
            payload['controllers'].append({'name': 'boiler', 'value': True})
        elif boiler_temperature > hot_water_ok_temp:
            payload['controllers'].append({'name': 'boiler', 'value': False})
        if bedroom_temperature > bedroom_high_temp:
            payload['controllers'].append({'name': 'air_conditioner', 'value': True})
        elif bedroom_temperature < bedroom_low_temp:
            payload['controllers'].append({'name': 'air_conditioner', 'value': False})

    curtains = controller_data['curtains']['value']
    outdoor_light = controller_data['outdoor_light']['value']
    bedroom_light = controller_data['bedroom_light']['value']
    db_bedroom_light = Setting.objects.get(
        controller_name='bedroom_light'
    ).value
    if curtains == 'slightly_open':
        pass
    else:
        if outdoor_light < 50 and not bedroom_light:
            if bedroom_light != db_bedroom_light:
                payload['controllers'].append({'name': 'curtains', 'value': 'open'})
        elif outdoor_light > 50 or bedroom_light:
            if bedroom_light != db_bedroom_light:
                payload['controllers'].append({'name': 'curtains', 'value': 'close'})
    requests.post(url, headers=headers, json=payload)
