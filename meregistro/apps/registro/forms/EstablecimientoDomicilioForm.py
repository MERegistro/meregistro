# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstablecimientoDomicilio import EstablecimientoDomicilio
from apps.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoDomicilioForm(forms.ModelForm):

    class Meta:
        model = EstablecimientoDomicilio
        exclude = ['establecimiento']
