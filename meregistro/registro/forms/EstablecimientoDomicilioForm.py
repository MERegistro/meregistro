# -*- coding: utf-8 -*-
from django.forms import ModelForm
from meregistro.registro.models.Establecimiento import Establecimiento
from meregistro.registro.models.EstablecimientoDomicilio import EstablecimientoDomicilio
from meregistro.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoDomicilioForm(forms.ModelForm):

    class Meta:
        model = EstablecimientoDomicilio
        exclude = ['establecimiento']
