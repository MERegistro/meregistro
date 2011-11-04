# -*- coding: utf-8 -*-
from apps.registro.models.AnexoConexionInternet import AnexoConexionInternet
from apps.registro.models.TipoConexion import TipoConexion
from django.core.exceptions import ValidationError
from django import forms


class AnexoConexionInternetForm(forms.ModelForm):
    tipo_conexion = forms.ModelChoiceField(queryset = TipoConexion.objects.all().order_by('nombre'), required = True)

    class Meta:
        model = AnexoConexionInternet
        exclude = ['anexo']
