# -*- coding: utf-8 -*-
from django.forms import ModelForm
from meregistro.registro.models.UnidadExtension import UnidadExtension
from meregistro.registro.models.UnidadExtensionDomicilio import UnidadExtensionDomicilio
from meregistro.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class UnidadExtensionDomicilioForm(forms.ModelForm):

    class Meta:
        model = UnidadExtensionDomicilio
