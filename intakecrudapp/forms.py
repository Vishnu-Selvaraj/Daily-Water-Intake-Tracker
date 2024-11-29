from django import forms
from .models import WaterInke


class WaterIntakeForm(forms.ModelForm):
    class Meta:
        model = WaterInke
        fields = ['quantity']