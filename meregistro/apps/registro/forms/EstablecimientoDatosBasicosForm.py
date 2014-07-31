# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from apps.registro.forms import EstablecimientoCreateForm
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoDatosBasicosForm(EstablecimientoCreateForm):

    class Meta:
        model = Establecimiento
        fields = ['dependencia_funcional', 'nombre', 'unidad_academica', 'nombre_unidad_academica', \
            'subsidio', 'anio_creacion', 'tipo_normativa', 'tipo_norma', 'tipo_norma_otra', 'norma_creacion', 'observaciones']


    def __init__(self, *args, **kwargs):
        super(EstablecimientoCreateForm, self).__init__(*args, **kwargs)
        self.fields['codigo_jurisdiccion'].required = False
        self.fields['cue'].required = False
        self.fields['codigo_tipo_unidad_educativa'].required = False

    def clean_cue(self):
        return
