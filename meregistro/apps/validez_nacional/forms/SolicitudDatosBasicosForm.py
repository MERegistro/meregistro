# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Carrera, EstadoCarrera, TituloNacional
from apps.validez_nacional.models import Solicitud


class SolicitudDatosBasicosForm(forms.ModelForm):
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.order_by('nombre'), label='Título', required=True)
	titulo_nacional = forms.ModelChoiceField(queryset=TituloNacional.objects.order_by('nombre'), label='Título', required=True)
	
	class Meta:
	   model = Solicitud
	   fields = ('carrera', 'titulo_nacional',)

	def __init__(self, *args, **kwargs):
		jurisdiccion_id = kwargs.pop('jurisdiccion_id')
		try:
			solicitud = kwargs.pop('instance')
		except KeyError:
			solicitud = None
		super(SolicitudDatosBasicosForm, self).__init__(*args, **kwargs)
		self.fields['carrera'].queryset = self.fields['carrera'].queryset.filter(jurisdicciones__id=jurisdiccion_id, estado__nombre=EstadoCarrera.VIGENTE)
		if solicitud:
			self.initial = {'carrera': solicitud.carrera, 'titulo_nacional': solicitud.titulo_nacional}
