from __future__ import absolute_import, unicode_literals
from celery import task

from .models import Setting

@task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    pass
