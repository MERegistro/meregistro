# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.validez_nacional.models import Solicitud, EstadoSolicitud


class SolicitudControlForm(forms.ModelForm):
	dictamen_cofev = forms.CharField(max_length=200, label='Dictámen Cofev', required=True)
	normativas_nacionales = forms.CharField(max_length=99, label='Normativas Nacionales', required=True)
	estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.order_by('nombre'), label='Estado', required=True)
	
	class Meta:
	   model = Solicitud
	   fields = ('dictamen_cofev', 'normativas_nacionales', 'estado')

	def __init__(self, *args, **kwargs):
		super(SolicitudControlForm, self).__init__(*args, **kwargs)
