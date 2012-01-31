# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from apps.registro.models import Establecimiento, Jurisdiccion
from django.core.exceptions import ValidationError


class EstablecimientoForm(ModelForm):
    codigo_jurisdiccion = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cue = forms.CharField(label='CUE', required=True, widget=forms.TextInput(attrs={'size': 5, 'maxlength': 5}))
    codigo_tipo_unidad_educativa = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    anio_creacion = forms.IntegerField(label='Año de creación', required=False, widget=forms.TextInput(attrs={'size': 4, 'maxlength': 4}))

    class Meta:
        model = Establecimiento

    def clean_anio_creacion(self):
        # Ya fue validado que se introduzcan sólo enteros
        anio_creacion = self.cleaned_data['anio_creacion']
        if anio_creacion is not None:
            anio_creacion = int(anio_creacion)
            if anio_creacion < 1000 or anio_creacion > 9999:
                raise ValidationError('El año tiene que tener cuatro dígitos')
        else:
            return
        return anio_creacion
        
    def clean_nombre_unidad_academica(self):
        unidad_academica = self.cleaned_data['unidad_academica']
        nombre_unidad_academica = self.cleaned_data['nombre_unidad_academica']
        if unidad_academica and nombre_unidad_academica == '':
            raise ValidationError('Por favor ingrese el nombre de la unidad académica')
        return nombre_unidad_academica

    def clean_cue(self):
        cue = self.cleaned_data['cue']
        try:
            intval = int(cue)
        except ValueError:
            raise ValidationError('Por favor ingrese sólo números positivos')
        if int(cue) < 0:
            raise ValidationError('Por favor ingrese sólo números positivos') 
        if len(cue) != 5:
            raise ValidationError('El CUE debe tener 9 dígitos en total') 
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
