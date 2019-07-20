from __future__ import absolute_import, unicode_literals
import requests
from celery import task
from django.conf import settings
from .models import Setting


TOKEN = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {TOKEN}'}


@task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    controller_data = requests.get(url, headers=headers).json().get('data')
    if controller_data:
        controller_data = {x['name']: x for x in controller_data}

        water_leaks = controller_data['leak_detector']['value']
        if water_leaks:
            payload = {
                'controllers': [
                    {'name': 'cold_water', 'value': False},
                    {'name': 'hot_water', 'value': False}
                ]
            }
            requests.post(url, headers=headers, json=payload)

        cold_water_on = controller_data['cold_water']['value']
        if not cold_water_on:
            payload = {
                'controllers': [
                    {'name': 'boiler', 'value': False},
                    {'name': 'washing_machine', 'value': "off"}
                ]
            }
            requests.post(url, headers=headers, json=payload)

        boiler_temperature = controller_data['boiler_temperature']['value']
        hot_water_target_temperature = Setting.objects.get(
            controller_name='hot_water_target_temperature').value
        hot_water_low_temp = hot_water_target_temperature - hot_water_target_temperature * 0.1
        hot_water_ok_temp = hot_water_target_temperature + hot_water_target_temperature * 0.1

        bedroom_temperature = controller_data['bedroom_temperature']['value']
        bedroom_target_temperature = Setting.objects.get(
            controller_name='bedroom_target_temperature').value
        bedroom_low_temp = bedroom_target_temperature - bedroom_target_temperature * 0.1
        bedroom_ok_temp = bedroom_target_temperature + bedroom_target_temperature * 0.1

        smoke_detector = controller_data['smoke_detector']['value']

        if smoke_detector:
            payload = {
                'controllers': [
                    {'name': 'air_conditioner', 'value': False},
                    {'name': 'bedroom_light', 'value': False},
                    {'name': 'bathroom_light', 'value': False},
                    {'name': 'boiler', 'value': False},
                    {'name': 'washing_machine', 'value': 'off'},
                ]
            }
            requests.post(url, headers=headers, json=payload)
        else:
            if boiler_temperature < hot_water_low_temp:
                payload = {
                    'controllers': [
                        {'name': 'boiler', 'value': True},
                    ]
                }
                requests.post(url, headers=headers, json=payload)
            elif boiler_temperature > hot_water_ok_temp:
                payload = {
                    'controllers': [
                        {'name': 'boiler', 'value': False},
                    ]
                }
                requests.post(url, headers=headers, json=payload)
            if bedroom_temperature > bedroom_ok_temp:
                payload = {
                    'controllers': [
                        {'name': 'air_conditioner', 'value': True},
                    ]
                }
                requests.post(url, headers=headers, json=payload)
            elif bedroom_temperature < bedroom_low_temp:
                payload = {
                    'controllers': [
                        {'name': 'air_conditioner', 'value': False},
                    ]
                }
                requests.post(url, headers=headers, json=payload)

        curtains = controller_data['curtains']['value']
        outdoor_light = controller_data['outdoor_light']['value']
        bedroom_light = Setting.objects.get(
            controller_name='bedroom_light'
        ).value
        if curtains == 'slightly_open':
            pass
        else:
            if outdoor_light < 50:
                if not bedroom_light:
                    payload = {
                        'controllers': [
                            {'name': 'curtains', 'value': 'open'},
                        ]
                    }
                    requests.post(url, headers=headers, json=payload)
            elif outdoor_light > 50 or bedroom_light:
                payload = {
                    'controllers': [
                        {'name': 'curtains', 'value': 'close'},
                    ]
                }
                requests.post(url, headers=headers, json=payload)
