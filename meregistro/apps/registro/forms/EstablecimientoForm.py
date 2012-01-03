# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from apps.registro.models import Establecimiento, Jurisdiccion
from django.core.exceptions import ValidationError


class EstablecimientoForm(ModelForm):
    codigo_jurisdiccion = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cue = forms.CharField(label='CUE', required=True, widget=forms.TextInput(attrs={'size': 5, 'maxlength': 5}))
    codigo_tipo_unidad_educativa = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Establecimiento

    def clean_anio_creacion(self):
        anio_creacion = self.cleaned_data['anio_creacion']
        try:
            if(anio_creacion is not None):
                anio_creacion = int(anio_creacion)
        except ValidationError:
            pass
        return anio_creacion

    def clean_cue(self):
        cue = self.cleaned_data['cue']
        try:
            intval = int(cue)
        except ValueError:
            raise ValidationError('Por favor ingrese sólo números')  # Para dar un mensaje más claro
        if len(cue) != 5:
            raise ValidationError('El CUE debe tener 9 dígitos en total')  # Para dar un mensaje más claro
        return cue

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
