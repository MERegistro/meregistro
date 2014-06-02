# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import CarreraPostitulo, EstadoCarreraPostitulo, PostituloNacional
from apps.postitulos.models import Solicitud


class SolicitudDatosBasicosForm(forms.ModelForm):
	carrera_postitulo = forms.ModelChoiceField(queryset=CarreraPostitulo.objects.order_by('nombre'), label='Carrera', required=True)
	postitulo_nacional = forms.ModelChoiceField(queryset=PostituloNacional.objects.order_by('nombre'), label='Postítulo', required=True)
	
	class Meta:
	   model = Solicitud
	   fields = ('carrera_postitulo', 'postitulo_nacional',)

	def __init__(self, *args, **kwargs):
		jurisdiccion_id = kwargs.pop('jurisdiccion_id')
		try:
			solicitud = kwargs.pop('instance')
		except KeyError:
			solicitud = None
		super(SolicitudDatosBasicosForm, self).__init__(*args, **kwargs)
		self.fields['carrera_postitulo'].queryset = self.fields['carrera_postitulo'].queryset.filter(jurisdicciones__id=jurisdiccion_id, estado__nombre=EstadoCarreraPostitulo.VIGENTE)#, carrera_sin_orientacion=True)
		if solicitud:
			self.initial = {'carrera_postitulo': solicitud.carrera_postitulo, 'postitulo_nacional': solicitud.postitulo_nacional}
