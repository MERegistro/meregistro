# -*- coding: utf-8 -*-
from apps.registro.models.EstablecimientoConexionInternet import EstablecimientoConexionInternet
from apps.registro.models.TipoConexion import TipoConexion
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoConexionInternetForm(forms.ModelForm):
    tipo_conexion = forms.ModelChoiceField(queryset = TipoConexion.objects.all().order_by('nombre'), required = True)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = EstablecimientoConexionInternet
        exclude = ['establecimiento']
