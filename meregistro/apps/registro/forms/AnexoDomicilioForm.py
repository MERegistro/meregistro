# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Anexo import Anexo
from apps.registro.models.AnexoDomicilio import AnexoDomicilio
from apps.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class AnexoDomicilioForm(forms.ModelForm):

    class Meta:
        model = AnexoDomicilio
        exclude = ('anexo')
