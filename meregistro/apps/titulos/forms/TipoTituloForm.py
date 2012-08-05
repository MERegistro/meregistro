# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from apps.titulos.models import TipoTitulo

class TipoTituloForm(ModelForm):
    class Meta:
        model = TipoTitulo
