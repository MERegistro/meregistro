# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.Turno import Turno
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


currentYear = datetime.datetime.now().year
norma_creacion_choices = [('', 'Seleccione...')] + [(k, k) for k in ExtensionAulica.NORMA_CREACION_CHOICES]


class ExtensionAulicaForm(forms.ModelForm):
    codigo_jurisdiccion = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cue = forms.CharField(max_length=5, label='CUE', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    codigo_tipo_unidad_educativa = forms.CharField(label='', required=False, help_text=u'2 dígitos, ej: 01...02', widget=forms.TextInput(attrs={'size': 2, 'maxlength': 2}))
    norma_creacion = forms.ChoiceField(label='Norma de creación', choices=norma_creacion_choices, required=True)
    norma_creacion_otra = forms.CharField(required=False)
    observaciones = forms.CharField(required=False, widget=forms.Textarea)
    verificado = forms.BooleanField(required=False)
    anio_creacion = forms.ChoiceField(choices=[('', 'Seleccione...')] + ExtensionAulica.YEARS_CHOICES, required=False)
      

    class Meta:
        model = ExtensionAulica
        exclude = ('estado', 'funciones', 'alcances', 'turnos', 'sitio_web', 'telefono', 'email', 'normativa', 'tipo_normativa')

    def clean_codigo_tipo_unidad_educativa(self):
        codigo = self.cleaned_data['codigo_tipo_unidad_educativa']
        if codigo != '':
            try:
                intval = int(codigo)
            except ValueError:
                raise ValidationError('Por favor ingrese sólo números positivos')
            if int(codigo) < 1:
                raise ValidationError('Por favor ingrese sólo números positivos') 
            if len(codigo) != 2:
                raise ValidationError('El Código debe tener 2 dígitos')
        return codigo

    def clean_anio_creacion(self):
        # Ya fue validado que se introduzcan sólo enteros
        anio_creacion = self.cleaned_data['anio_creacion']
        if anio_creacion != '' and anio_creacion is not None:
            anio_creacion = int(anio_creacion)
            if anio_creacion < 1000 or anio_creacion > 9999:
                raise ValidationError('El año tiene que tener cuatro dígitos')
        return anio_creacion
            
    def clean_norma_creacion_otra(self):
        try:
            norma_creacion = self.cleaned_data['norma_creacion']
            norma_creacion_otra = self.cleaned_data['norma_creacion_otra']
            if norma_creacion == 'Otra' and norma_creacion_otra == '':
                raise ValidationError('Por favor escriba la norma de creación')
        except KeyError:
            norma_creacion_otra = ''
        return norma_creacion_otra

    def clean(self):
        # Armar el CUE correctamente, si no se especificó código, no cargarlo
        cleaned_data = self.cleaned_data
        try:
            if cleaned_data['codigo_tipo_unidad_educativa'] == '':
                cleaned_data['cue'] = ''
            else:
                cue = str(cleaned_data['cue'])
                codigo_jurisdiccion = cleaned_data['codigo_jurisdiccion']
                codigo_tipo_unidad_educativa = cleaned_data['codigo_tipo_unidad_educativa']
                cleaned_data['cue'] = str(codigo_jurisdiccion) + str(cue) + str(codigo_tipo_unidad_educativa)
        except KeyError:
            pass
        return cleaned_data
