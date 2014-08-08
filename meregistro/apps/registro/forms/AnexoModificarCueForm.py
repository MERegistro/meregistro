# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Anexo, Establecimiento
from apps.registro.forms import AnexoCreateForm
from django.core.exceptions import ValidationError
from django import forms


class AnexoModificarCueForm(AnexoCreateForm):

    class Meta:
        model = Anexo
        fields = ['codigo_tipo_unidad_educativa', 'cue', 'codigo_jurisdiccion']


    def __init__(self, *args, **kwargs):
        super(AnexoModificarCueForm, self).__init__(*args, **kwargs)

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

