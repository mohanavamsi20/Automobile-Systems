from django import forms

from .models import *

class DealsModelForm(forms.ModelForm):
    class Meta:
        model = Deals
        fields = '__all__'

class CustomsModelForm(forms.ModelForm):
    class Meta:
        model = Custom
        fields = '__all__'