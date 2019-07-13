from __future__ import absolute_import, unicode_literals
import requests
from celery import task
from django.conf import settings
from .models import Setting


@task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    print('yay')
    pass


TOKEN = settings.SMART_HOME_ACCESS_TOKEN
url = settings.SMART_HOME_API_URL
headers = {'Authorization': f'Bearer {TOKEN}'}


@task()
def poll_controller():
    r = requests.get(url, headers=headers)
    return r.json()
