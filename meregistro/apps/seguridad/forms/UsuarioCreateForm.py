# -*- coding: UTF-8 -*-

from django import forms
from django.forms import ModelForm
from apps.seguridad.models import Ambito, Rol, Usuario


class UsuarioCreateForm(ModelForm):
    class Meta:
        model = Usuario

    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')
    repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Repetir contraseña')
    rol = forms.ModelChoiceField(queryset=Rol.objects, label='rol')
    ambito = forms.ModelChoiceField(queryset=Ambito.objects, label='ambito')

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
            self._errors['password'] = self.error_class([u'Las contraseñas no coinciden'])
        if self.cleaned_data.has_key('rol') and self.cleaned_data.has_key('ambito') and not self.cleaned_data['rol'].asignableAAmbito(self.cleaned_data['ambito']):
            self._errors['rol'] = self.error_class([u'El rol no puede asignarse al ámbito seleccionado'])
        return self.cleaned_data
