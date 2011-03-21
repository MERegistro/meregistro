# -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm
from seguridad.models import Ambito, Rol, Usuario

class UsuarioCreateForm(ModelForm):
  class Meta:
    model = Usuario

  password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')
  repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Repetir contraseña')
  rol = forms.ModelChoiceField(queryset=Rol.objects, label='rol')
  ambito = forms.ModelChoiceField(queryset=Ambito.objects, label='ambito')
