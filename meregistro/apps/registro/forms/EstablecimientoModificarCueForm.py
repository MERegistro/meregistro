# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from apps.registro.forms import EstablecimientoCreateForm
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoModificarCueForm(EstablecimientoCreateForm):

    class Meta:
        model = Establecimiento
        fields = ['cue']


    def __init__(self, *args, **kwargs):
        super(EstablecimientoCreateForm, self).__init__(*args, **kwargs)

    def clean(self):
        # Armar el CUE correctamente
        cleaned_data = self.cleaned_data
        try:
            cue = str(cleaned_data['cue'])
            codigo_jurisdiccion = cleaned_data['codigo_jurisdiccion']
            codigo_tipo_unidad_educativa = cleaned_data['codigo_tipo_unidad_educativa']
            cleaned_data['cue'] = str(codigo_jurisdiccion) + str(cue) + str(codigo_tipo_unidad_educativa)
        except KeyError:
            pass
        return cleaned_data
