# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Anexo
from django.core.exceptions import ValidationError
from django import forms


class AnexoContactoForm(ModelForm):
    class Meta:
        model = Anexo
        fields = ['telefono', 'interno', 'fax', 'sitio_web', 'email']

    def clean(self):
        telefono = self.cleaned_data['telefono']
        interno = self.cleaned_data['interno']
        if interno and telefono == '':
            raise ValidationError('Por favor ingrese el número de teléfono')
            
        return self.cleaned_data
