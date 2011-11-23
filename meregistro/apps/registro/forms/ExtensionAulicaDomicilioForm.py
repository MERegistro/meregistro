# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.ExtensionAulicaDomicilio import ExtensionAulicaDomicilio
from apps.registro.models.TipoDomicilio import TipoDomicilio
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaDomicilioForm(forms.ModelForm):

    class Meta:
        model = ExtensionAulicaDomicilio
