# -*- coding: utf-8 -*-
from django.forms import ModelForm
from registro.models import Establecimiento
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoDatosBasicosForm(ModelForm):

    class Meta:
        model = Establecimiento
        fields = ['tipo_normativa', 'norma_creacion', 'anio_creacion', 'unidad_academica', 'nombre_unidad_academica', 'sitio_web', 'email', 'telefono']
