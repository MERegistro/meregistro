# -*- coding: utf-8 -*-
from django.forms import ModelForm
from meregistro.apps.registro.models.Anexo import Anexo
from meregistro.apps.registro.models.AnexoDomicilio import AnexoDomicilio
from meregistro.apps.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class AnexoDomicilioForm(forms.ModelForm):

    class Meta:
        model = AnexoDomicilio
        exclude = ('anexo')
