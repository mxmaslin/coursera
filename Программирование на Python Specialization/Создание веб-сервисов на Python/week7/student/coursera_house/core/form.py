from django import forms


class ControllerForm(forms.Form):
    bedroom_target_temperature = forms.IntegerField()
    hot_water_target_temperature = forms.IntegerField()
    bedroom_light = forms.BooleanField()
    bathroom_light = forms.BooleanField()
