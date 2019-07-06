Coursera House
==============

Это шаблон курсового проекта от преподавателей курса.


Установка
---------

Установите pipenv https://docs.pipenv.org/

.. code-block:: bash

    $ pip install pipenv


Установите зависимости проекта, включая зависимости для разработки

.. code-block:: bash

    $ pipenv install --dev

Активируйте virtualenv проекта

.. code-block:: bash

    $ pipenv shell

Запустите миграции

.. code-block:: bash

    $ python manage.py migrate

И приступайте к разработке.


Запуск
------

На главной странице сервиса будет расположена панель управления вашим умным домом.

Для запуска периодического опроса состояния дома, используется celery.

Она запускается как celery -A coursera_house.celery worker -l info -B

Celery использует Redis как брокер, инструкция по установке Redis: https://redis.io/topics/quickstart


Тестирование
------------


Для запуска тестов выполните команду

.. code-block:: bash

    $ py.test tests
