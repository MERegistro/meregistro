# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Anexo
from django.core.exceptions import ValidationError
from django import forms


class AnexoDatosBasicosForm(ModelForm):
    class Meta:
        model = Anexo
        fields = ['sitio_web', 'email', 'telefono']
