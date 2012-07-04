# -*- coding: utf-8 -*-
from apps.registro.models.ExtensionAulicaConexionInternet import ExtensionAulicaConexionInternet
from apps.registro.models.TipoConexion import TipoConexion
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaConexionInternetForm(forms.ModelForm):
  tipo_conexion = forms.ModelChoiceField(queryset = TipoConexion.objects.all().order_by('nombre'), required = False)
  verificado = forms.BooleanField(required=False)

  class Meta:
    model = ExtensionAulicaConexionInternet
    exclude = ['extension_aulica']

  def __chequear_si_tiene_conexion(self, field):
    if self.cleaned_data['tiene_conexion']:
      if (self.cleaned_data[field] is None
      or self.cleaned_data[field] == ''):
        raise ValidationError('Este campo es obligatorio.')
      return self.cleaned_data[field]
    return None

  def clean_tipo_conexion(self):
    return self.__chequear_si_tiene_conexion('tipo_conexion')

  def clean_proveedor(self):
    return self.__chequear_si_tiene_conexion('proveedor')

  def clean_costo(self):
    return self.__chequear_si_tiene_conexion('costo')

  def clean_cantidad(self):
    return self.__chequear_si_tiene_conexion('cantidad')
