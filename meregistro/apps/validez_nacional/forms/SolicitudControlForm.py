# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.validez_nacional.models import Solicitud, EstadoSolicitud
from django.core.validators import RegexValidator

class SolicitudControlForm(forms.ModelForm):
    nro_expediente = forms.CharField(max_length=200, label='Nro. Expediente', required=False, validators=[
        RegexValidator(
            '^.*\/[0-9]{2}$', 
            message='El Nro de Expediente debe incluir dos dígitos indicando el año (ej: abcde/14)', 
            code='expediente_invalido'
        ),
    ])
    dictamen_cofev = forms.CharField(max_length=200, label='Dictamen Cofev', required=False)
    normativas_nacionales = forms.CharField(max_length=99, label='Normativas Nacionales', required=False)
    estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.order_by('nombre'), label='Estado', required=True, empty_label=None)
    
    class Meta:
       model = Solicitud
       fields = ('dictamen_cofev', 'normativas_nacionales', 'estado', 'nro_expediente')

    def __init__(self, *args, **kwargs):
        super(SolicitudControlForm, self).__init__(*args, **kwargs)
        # No se puede pasar a estado numerado por esta vía
        self.fields['estado'].queryset = EstadoSolicitud.objects.exclude(nombre=EstadoSolicitud.NUMERADO)


    def clean(self):
        data = self.cleaned_data
        '''
        REGLAS:
        -------
        PENDIENTE: sin requerimientos
        CONTROLADO: Nro Exp
        RETENIDO: Nro Exp
        EVALUADO: Dictamen COFEV
        NUMERADO: (se pasa en la numeración)
        '''
        estado = data['estado'].nombre
        normativas_nacionales = data['normativas_nacionales']
        dictamen_cofev = data['dictamen_cofev']
        nro_expediente = data['nro_expediente']
        
        if estado == EstadoSolicitud.CONTROLADO and nro_expediente == '':
            raise forms.ValidationError(u'Para pasar a estado "controlado", es necesario cargar el número de expediente')
        if estado == EstadoSolicitud.RETENIDO and nro_expediente == '':
            raise forms.ValidationError(u'Para pasar a estado "retenido", es necesario cargar el número de expediente')
        if estado == EstadoSolicitud.EVALUADO and dictamen_cofev == '':
            raise forms.ValidationError(u'Para pasar a estado "evaluado", es necesario cargar el dictámen COFEV')
        #if estado == EstadoSolicitud.NUMERADO and normativas_nacionales == '':
        #    raise forms.ValidationError(u'Para pasar a estado "numerado", es necesario cargar las normativas nacionales')
        return self.cleaned_data
