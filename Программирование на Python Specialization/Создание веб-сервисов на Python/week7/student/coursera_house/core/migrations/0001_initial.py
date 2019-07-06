# -*- coding: utf-8 -*-
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('controller_name', models.CharField(max_length=40)),
                ('label', models.CharField(max_length=100)),
                ('value', models.IntegerField(default=20)),
            ],
        ),
    ]
