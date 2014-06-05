__author__ = 'leonardo'
#encoding:utf-8
from django.forms import ModelForm, PasswordInput
from django import forms
from django.contrib.auth.models import User

class EmailForm(forms.Form):
    email = forms.EmailField()
    nombre = forms.CharField()
    apellido = forms.CharField()

class InvitacionForm(forms.Form):
    email = forms.EmailField()

class TorneoForm(forms.Form):
    nombre = forms.CharField()