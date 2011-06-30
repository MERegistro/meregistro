# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.UnidadExtension import UnidadExtension
from apps.registro.models.UnidadExtensionDomicilio import UnidadExtensionDomicilio
from apps.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class UnidadExtensionDomicilioForm(forms.ModelForm):

    class Meta:
        model = UnidadExtensionDomicilio
