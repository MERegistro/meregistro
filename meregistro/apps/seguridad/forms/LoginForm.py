# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import TipoDocumento, Usuario
import re
from apps.seguridad.authenticate import *


class LoginForm(forms.Form):
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects, required=True)
    documento = forms.CharField(max_length=20, label='documento')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')

    def clean_documento(self):
        '''
        Chequea que el usuario exista en la base de datos
        '''
        documento = self.cleaned_data['documento']
        if not re.search(r'^\w+$', documento):
            raise forms.ValidationError(u'Este campo sólo puede contener letras del alfabeto y números')
        try:
            Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            raise forms.ValidationError(u'Usuario inexistente')
        return documento

    def clean(self):
        '''
        Chequeos posteriores en los
        que puede haber varios campos involucrados
        '''
        cleaned_data = self.cleaned_data
        tipo_documento = cleaned_data.get("tipo_documento")
        documento = cleaned_data.get("documento")
        password = cleaned_data.get("password")

        # Chequea si el password corresponde al usuario
        if documento and password:
            res = authenticate(tipo_documento, documento, password)
            if  res == False:
                self._errors['password'] = self.error_class([u'Password erróneo'])
        return cleaned_data
