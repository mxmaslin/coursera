from django.db import migrations


def create_initial_settings(apps, schema_editor):
    Setting = apps.get_model('core', 'Setting')
    Setting.objects.bulk_create([
        Setting(
            controller_name='bedroom_target_temperature',
            label='Желаемая температура в спальне',
            value=21
        ),
        Setting(
            controller_name='hot_water_target_temperature',
            label='Желаемая температура горячей воды',
            value=80
        )
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_settings),
    ]
