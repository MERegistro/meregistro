# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import TipoDocumento, Usuario
import re
from apps.seguridad.authenticate import *


class LoginForm(forms.Form):
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.order_by('abreviatura'), required=True, empty_label=None)
    documento = forms.CharField(max_length=8, label='documento')
    password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')

    def clean_documento(self):
        '''
        Chequea que el usuario exista en la base de datos
        '''
        self.cleaned_data['documento']
        documento = self.cleaned_data['documento']
        if not re.search(r'^\w+$', documento):
            raise forms.ValidationError(u'Este campo sólo puede contener letras del alfabeto y números')
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
        if password is not None:
            password = password.strip()

        # Chequea si el password corresponde al usuario
        if documento and password:
            res = authenticate(tipo_documento, documento, password)
            if  res == False:
                raise forms.ValidationError('Los datos ingresados son incorrectos.')
        return cleaned_data
