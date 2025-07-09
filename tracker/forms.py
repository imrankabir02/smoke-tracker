from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Brand, SmokeLog, DailyGoal, UserDefault, UserBrand, Profile
from zoneinfo import available_timezones

class SignUpForm(UserCreationForm):
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in sorted(available_timezones())],
                                 widget=forms.Select(attrs={'class': 'form-select'}))
    currency = forms.CharField(max_length=10,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., USD'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class ProfileForm(forms.ModelForm):
    timezone = forms.ChoiceField(choices=[(tz, tz) for tz in sorted(available_timezones())],
                                 widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Profile
        fields = ['timezone', 'currency']
        widgets = {
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Marlboro Red'
            }),
        }

class UserBrandForm(forms.ModelForm):
    class Meta:
        model = UserBrand
        fields = ['brand', 'price']
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': 'e.g., 12.50'
            }),
        }

class SmokeLogForm(forms.ModelForm):
    class Meta:
        model = SmokeLog
        fields = ['user_brand', 'trigger', 'mood_before', 'mood_after', 'note']
        widgets = {
            'user_brand': forms.Select(attrs={'class': 'form-select'}),
            'trigger': forms.Select(attrs={'class': 'form-select'}),
            'mood_before': forms.Select(attrs={'class': 'form-select'}),
            'mood_after': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional notes about this smoke...'
            }),
        }

class DailyGoalForm(forms.ModelForm):
    class Meta:
        model = DailyGoal
        fields = ['daily_limit']
        widgets = {
            'daily_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '50',
                'placeholder': 'e.g., 10'
            }),
        }
        labels = {
            'daily_limit': 'Daily Smoking Limit'
        }

class UserDefaultForm(forms.ModelForm):
    class Meta:
        model = UserDefault
        fields = ['user_brand', 'trigger', 'mood_before', 'mood_after']
        widgets = {
            'user_brand': forms.Select(attrs={'class': 'form-select'}),
            'trigger': forms.Select(attrs={'class': 'form-select'}),
            'mood_before': forms.Select(attrs={'class': 'form-select'}),
            'mood_after': forms.Select(attrs={'class': 'form-select'}),
        }
