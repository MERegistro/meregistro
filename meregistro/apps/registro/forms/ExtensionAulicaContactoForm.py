# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import ExtensionAulica
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaContactoForm(ModelForm):

    class Meta:
        model = ExtensionAulica
        fields = ['telefono','sitio_web', 'email']

