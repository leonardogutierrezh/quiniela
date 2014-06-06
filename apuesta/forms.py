from django.forms import ModelForm, PasswordInput
from django import forms
from django.contrib.auth.models import User

class partidosForms(forms.Form):
    equipoL = forms.IntegerField()
    equipoV = forms.IntegerField()