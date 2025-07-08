from django import forms
from .models import SmokeLog, Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'price']

class SmokeLogForm(forms.ModelForm):
    class Meta:
        model = SmokeLog
        fields = ['brand', 'note']
