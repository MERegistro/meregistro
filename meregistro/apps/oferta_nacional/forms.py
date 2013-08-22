# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Jurisdiccion, Establecimiento, EstablecimientoDomicilio
from apps.titulos.models import Cohorte, CohorteEstablecimiento, CarreraJurisdiccional, Carrera


class OfertaNacionalFormFilters(forms.Form):
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdiccion', required=False)
	cue = forms.CharField(max_length=40, label='Cue', required=False)
	establecimiento = forms.ModelChoiceField(queryset=Establecimiento.objects.order_by('nombre'), label='Nombre del ISFD', required=False)
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.order_by('nombre'), label='Carrera', required=False)	
	departamento = forms.CharField(max_length=40, label='Departamento', required=False)
	localidad = forms.CharField(max_length=40, label='Localidad', required=False)


	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = CohorteEstablecimiento.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('jurisdiccion'):
				q = q.filter(establecimiento__dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
			if filter_by('cue'):
				q = q.filter(establecimiento__cue=self.cleaned_data['cue'])
			if filter_by('establecimiento'):
				q = q.filter(establecimiento=self.cleaned_data['establecimiento'])
			if filter_by('carrera'):
				q = q.filter(cohorte__carrera_jurisdiccional__carrera=self.cleaned_data['carrera'])
			if filter_by('departamento'):
				q = q.filter(\
					establecimiento__domicilios__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					establecimiento__domicilios__localidad__departamento__nombre__icontains=self.cleaned_data['departamento'])
			if filter_by('localidad'):
				q = q.filter(\
					establecimiento__domicilios__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					establecimiento__domicilios__localidad__nombre__icontains=self.cleaned_data['localidad'])
		return q.distinct()
