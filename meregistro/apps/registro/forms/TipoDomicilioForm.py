# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from apps.registro.models import TipoDomicilio

class TipoDomicilioForm(ModelForm):
    class Meta:
        model = TipoDomicilio
