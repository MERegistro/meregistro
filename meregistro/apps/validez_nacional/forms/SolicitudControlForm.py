# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.validez_nacional.models import Solicitud, EstadoSolicitud
from django.core.validators import RegexValidator

class SolicitudControlForm(forms.ModelForm):
	nro_expediente = forms.CharField(max_length=200, label='Nro. Expediente', required=False, validators=[
		RegexValidator(
			'^.*\/[0-9]{2}$', 
			message='El Nro de Expediente debe incluir dos dígitos indicando el año (ej: abcde/14)', 
			code='expediente_invalido'
		),
	])
	dictamen_cofev = forms.CharField(max_length=200, label='Dictamen Cofev', required=False)
	normativas_nacionales = forms.CharField(max_length=99, label='Normativas Nacionales', required=False)
	estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.order_by('nombre'), label='Estado', required=True, empty_label=None)
	
	class Meta:
	   model = Solicitud
	   fields = ('dictamen_cofev', 'normativas_nacionales', 'estado', 'nro_expediente')

	def __init__(self, *args, **kwargs):
		super(SolicitudControlForm, self).__init__(*args, **kwargs)
		self.fields['estado'].queryset = EstadoSolicitud.objects.exclude(nombre=EstadoSolicitud.NUMERADO)


	def clean(self):
		data = self.cleaned_data
		'''
		No tiene que ser obligatoria si se carga número de expediente
		'''
		normativas_nacionales = data['normativas_nacionales']
		try:
			nro_expediente = data['nro_expediente']
		except KeyError:
			nro_expediente = None

		if nro_expediente and normativas_nacionales == '':
			raise forms.ValidationError(u'Las normativas nacionales son requeridas al cargar número de expediente.')
		'''
		Si se pasa a estado controlado, las normativas son obligatorias
		'''
		if data['estado'].nombre == EstadoSolicitud.CONTROLADO and normativas_nacionales == '':
			raise forms.ValidationError(u'Las normativas nacionales son requeridas al pasar a estado CONTROLADO.')
		return self.cleaned_data
