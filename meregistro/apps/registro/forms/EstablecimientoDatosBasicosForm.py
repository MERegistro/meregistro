# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoDatosBasicosForm(ModelForm):
    codigo_jurisdiccion = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cue = forms.CharField(label='CUE', required=True, widget=forms.TextInput(attrs={'size': 5, 'maxlength': 5}))
    codigo_tipo_unidad_educativa = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    observaciones = forms.CharField(max_length=255, required=False, widget=forms.Textarea)
    verificado = forms.BooleanField(required=False)
    anio_creacion = forms.ChoiceField(choices=[('', 'Seleccione...')] + Establecimiento.YEARS_CHOICES, required=False)

    class Meta:
        model = Establecimiento
        fields = ['dependencia_funcional', 'cue', 'nombre', 'unidad_academica', 'nombre_unidad_academica', \
            'subsidio', 'anio_creacion', 'tipo_normativa', 'tipo_norma', 'tipo_norma_otra', 'norma_creacion', 'observaciones']

    def clean_nombre_unidad_academica(self):
        unidad_academica = self.cleaned_data['unidad_academica']
        nombre_unidad_academica = self.cleaned_data['nombre_unidad_academica']
        if unidad_academica and nombre_unidad_academica == '':
            raise ValidationError('Por favor ingrese el nombre de la unidad académica')
        return nombre_unidad_academica

    def clean_tipo_norma_otra(self):
        try:
            tipo_norma = self.cleaned_data['tipo_norma']
            tipo_norma_otra = self.cleaned_data['tipo_norma_otra']
            if tipo_norma.descripcion == 'Otra' and tipo_norma_otra == '':
                raise ValidationError('Por favor escriba el tipo de norma')
        except KeyError:
            tipo_norma_otra = ''
            pass
        return tipo_norma_otra

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

