# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoContactoForm(ModelForm):
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = Establecimiento
        fields = ['telefono', 'interno', 'fax', 'sitio_web', 'email']

    def clean(self):
        telefono = self.cleaned_data['telefono']
        interno = self.cleaned_data['interno']
        if interno and telefono == '':
            raise ValidationError('Por favor ingrese el número de teléfono')
            
        return self.cleaned_data
