# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.validez_nacional.models import Solicitud, EstadoSolicitud


class SolicitudControlForm(forms.ModelForm):
	dictamen_cofev = forms.CharField(max_length=200, label='Dictamen Cofev', required=False)
	normativas_nacionales = forms.CharField(max_length=99, label='Normativas Nacionales', required=True)
	estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.order_by('nombre'), label='Estado', required=True, empty_label=None)
	
	class Meta:
	   model = Solicitud
	   fields = ('dictamen_cofev', 'normativas_nacionales', 'estado')

	def __init__(self, *args, **kwargs):
		super(SolicitudControlForm, self).__init__(*args, **kwargs)
		self.fields['estado'].queryset = EstadoSolicitud.objects.exclude(nombre=EstadoSolicitud.NUMERADO)
