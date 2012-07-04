# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Anexo import Anexo
from apps.registro.models.Turno import Turno
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


currentYear = datetime.datetime.now().year

class AnexoDatosBasicosForm(forms.ModelForm):
    codigo_jurisdiccion = forms.CharField(max_length=2, label='', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    cue = forms.CharField(max_length=5, label='CUE', required=True, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    codigo_tipo_unidad_educativa = forms.CharField(label='', required=True, help_text=u'2 dígitos, ej: 01...02', widget=forms.TextInput(attrs={'size': 2, 'maxlength': 2}))
    observaciones = forms.CharField(max_length=255, required=False, widget=forms.Textarea)
    verificado = forms.BooleanField(required=False)
    anio_creacion = forms.ChoiceField(choices=[('', 'Seleccione...')] + Anexo.YEARS_CHOICES, required=False)
    
    
    class Meta:
        model = Anexo
        exclude = ('estado', 'funciones', 'alcances', 'turnos', 'sitio_web', 'telefono', 'email',)


    def __init__(self, *args, **kwargs):
        super(AnexoDatosBasicosForm, self).__init__(*args, **kwargs)
        
        
    def clean_codigo_tipo_unidad_educativa(self):
        codigo = self.cleaned_data['codigo_tipo_unidad_educativa']
        try:
            intval = int(codigo)
        except ValueError:
            raise ValidationError('Por favor ingrese sólo números positivos')
        if int(codigo) < 1:
            raise ValidationError('Por favor ingrese sólo números positivos') 
        if len(codigo) != 2:
            raise ValidationError('El Código debe tener 2 dígitos')
        
        return codigo
        
    
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
        
        
    def clean_anio_creacion(self):
        anio_creacion = self.cleaned_data['anio_creacion']
        if anio_creacion == '':
            return
        return anio_creacion
        
    def clean_subsidio(self):
        from apps.registro.models import TipoSubsidio, TipoGestion
        subsidio = self.cleaned_data['subsidio']
        establecimiento = self.cleaned_data['establecimiento']
        tipo_gestion = establecimiento.dependencia_funcional.tipo_gestion.nombre
        if tipo_gestion == TipoGestion.ESTATAL and subsidio.descripcion != TipoSubsidio.SIN_SUBSIDIO:
            raise ValidationError('El Anexo no puede poseer subsidio ya que depende de una sede estatal')
        return subsidio


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
