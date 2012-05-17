# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import TipoDocumento, Usuario
import re
from apps.seguridad.authenticate import *


class RememberPasswordForm(forms.Form):
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.order_by('abreviatura'), required=True, empty_label=None)
    documento = forms.CharField(max_length=8, label='documento')

    def clean_documento(self):
        '''
        Chequea que el usuario exista en la base de datos
        '''
        self.cleaned_data['documento']
        documento = self.cleaned_data['documento']
        if not re.search(r'^\w+$', documento):
            raise forms.ValidationError(u'Este campo sólo puede contener letras del alfabeto y números')
        try:
            Usuario.objects.get(documento=documento)
        except Usuario.DoesNotExist:
            raise forms.ValidationError(u'Usuario inexistente')
        return documento
