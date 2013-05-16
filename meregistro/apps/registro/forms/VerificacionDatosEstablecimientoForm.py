# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Establecimiento

	
class VerificacionDatosEstablecimientoForm(forms.Form):
	unidad_educativa_id = forms.CharField(widget=forms.HiddenInput())
	dato_verificacion = forms.CharField(widget=forms.HiddenInput())
	return_url = forms.CharField(widget=forms.HiddenInput())
	verificado = forms.BooleanField(label='Datos Verificados')

	def __init__(self, *args, **kwargs):		
		self.dato_verificacion = kwargs.pop('dato_verificacion')
		self.unidad_educativa_id = kwargs.pop('unidad_educativa_id')
		self.return_url = kwargs.pop('return_url')
		verificado = kwargs.pop('verificado')
		super(VerificacionDatosEstablecimientoForm, self).__init__(*args, **kwargs)
		self.fields['unidad_educativa_id'].initial = self.unidad_educativa_id
		self.fields['dato_verificacion'].initial = self.dato_verificacion
		self.fields['return_url'].initial = self.return_url
		if verificado:
			self.fields['verificado'].widget.attrs['checked'] = 'checked'
