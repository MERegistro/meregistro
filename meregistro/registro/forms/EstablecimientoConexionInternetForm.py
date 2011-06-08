# -*- coding: utf-8 -*-
from meregistro.registro.models.EstablecimientoConexionInternet import EstablecimientoConexionInternet
from meregistro.registro.models.TipoConexion import TipoConexion
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoConexionInternetForm(forms.ModelForm):
    tipo_conexion = forms.ModelChoiceField(queryset = TipoConexion.objects.all().order_by('nombre'), required = True)

    class Meta:
        model = EstablecimientoConexionInternet
        exclude = ['establecimiento']
