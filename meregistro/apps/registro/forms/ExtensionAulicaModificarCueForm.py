# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import ExtensionAulica, Establecimiento
from apps.registro.forms import ExtensionAulicaCreateForm
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaModificarCueForm(ExtensionAulicaCreateForm):

    class Meta:
        model = ExtensionAulica
        fields = ['codigo_tipo_unidad_educativa', 'cue', 'codigo_jurisdiccion']


    def __init__(self, *args, **kwargs):
        super(ExtensionAulicaModificarCueForm, self).__init__(*args, **kwargs)
        self.fields['norma_creacion'].required = False

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

