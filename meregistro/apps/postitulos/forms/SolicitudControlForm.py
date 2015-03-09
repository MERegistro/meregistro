# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import Solicitud, EstadoSolicitud
from django.core.validators import RegexValidator

class SolicitudControlForm(forms.ModelForm):
    nro_expediente = forms.CharField(max_length=200, label='Nro. Expediente', required=False, validators=[
        RegexValidator(
            '^.*\/[0-9]{2}$', 
            message='El Nro de Expediente debe incluir dos dígitos indicando el año (ej: abcde/14)', 
            code='expediente_invalido'
        ),
    ])
    estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.order_by('nombre'), label='Estado', required=True, empty_label=None)
    normativas_postitulo = forms.CharField(max_length=99, label='Normativas Nacionales', required=False)
    
    
    class Meta:
       model = Solicitud
       fields = ('estado', 'normativas_postitulo', 'nro_expediente')

    def __init__(self, *args, **kwargs):
        super(SolicitudControlForm, self).__init__(*args, **kwargs)
        self.fields['estado'].queryset = EstadoSolicitud.objects.exclude(nombre=EstadoSolicitud.NUMERADO)


    def clean(self):
        data = self.cleaned_data
        '''
        Si se pasa a estado controlado, el nro exp. es obligatorio
        '''
        try:
            nro_expediente = data['nro_expediente']
            if data['estado'].nombre == EstadoSolicitud.CONTROLADO and nro_expediente == '':
                raise forms.ValidationError(u'El Nro. de Expediente es requerido al pasar a estado CONTROLADO.')
        except KeyError:
            pass
        return self.cleaned_data
