# -*- coding: utf-8 -*-
from apps.registro.models.ExtensionAulicaConexionInternet import ExtensionAulicaConexionInternet
from apps.registro.models.TipoConexion import TipoConexion
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaConexionInternetForm(forms.ModelForm):
    tipo_conexion = forms.ModelChoiceField(queryset = TipoConexion.objects.all().order_by('nombre'), required = True)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = ExtensionAulicaConexionInternet
        exclude = ['extension_aulica']
