# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Jurisdiccion, Establecimiento, EstablecimientoDomicilio, TipoGestion
from apps.titulos.models import Cohorte, CohorteEstablecimiento, CarreraJurisdiccional, Carrera, CohorteAnexo, CohorteExtensionAulica


class OfertaNacionalFormFilters(forms.Form):
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdiccion', required=False)
	cue = forms.CharField(max_length=40, label='Cue', required=False)
	establecimiento = forms.ModelChoiceField(queryset=Establecimiento.objects.order_by('nombre'), label='Nombre del ISFD', required=False)
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.order_by('nombre'), label='Carrera', required=False)	
	tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.order_by('nombre'), label='Tipo de gestión', required=False)
	departamento = forms.CharField(max_length=40, label='Departamento', required=False)
	localidad = forms.CharField(max_length=40, label='Localidad', required=False)
	
	
	def __init__(self, *args, **kwargs):
		self.anio = kwargs.pop('anio')
		super(OfertaNacionalFormFilters, self).__init__(*args, **kwargs)


	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q1 = CohorteEstablecimiento.objects.filter(cohorte__anio=self.anio)
			q2 = CohorteAnexo.objects.filter(cohorte__anio=self.anio)
			q3 = CohorteExtensionAulica.objects.filter(cohorte__anio=self.anio)
			
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('jurisdiccion'):
				q1 = q1.filter(establecimiento__dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
				q2 = q2.filter(anexo__establecimiento__dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
				q3 = q3.filter(extension_aulica__establecimiento__dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
			if filter_by('cue'):
				q1 = q1.filter(establecimiento__cue=self.cleaned_data['cue'])
				q2 = q2.filter(anexo__cue=self.cleaned_data['cue'])
				q3 = q3.filter(extension_aulica__cue=self.cleaned_data['cue'])
			if filter_by('establecimiento'):
				q1 = q1.filter(establecimiento=self.cleaned_data['establecimiento'])
				q2 = q2.filter(anexo__establecimiento=self.cleaned_data['establecimiento'])
				q3 = q3.filter(extension_aulica__establecimiento=self.cleaned_data['establecimiento'])
			if filter_by('carrera'):
				q1 = q1.filter(cohorte__carrera_jurisdiccional__carrera=self.cleaned_data['carrera'])
				q2 = q2.filter(cohorte__carrera_jurisdiccional__carrera=self.cleaned_data['carrera'])
				q3 = q3.filter(cohorte__carrera_jurisdiccional__carrera=self.cleaned_data['carrera'])
			if filter_by('tipo_gestion'):
				q1 = q1.filter(establecimiento__dependencia_funcional__tipo_gestion__nombre=self.cleaned_data['tipo_gestion'].nombre)
				q2 = q2.filter(anexo__establecimiento__dependencia_funcional__tipo_gestion__nombre=self.cleaned_data['tipo_gestion'].nombre)
				q3 = q3.filter(extension_aulica__establecimiento__dependencia_funcional__tipo_gestion__nombre=self.cleaned_data['tipo_gestion'].nombre)
			if filter_by('departamento'):
				q1 = q1.filter(\
					establecimiento__domicilios__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					establecimiento__domicilios__localidad__departamento__nombre__icontains=self.cleaned_data['departamento'])
				q2 = q2.filter(\
					anexo__anexo_domicilio__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					anexo__anexo_domicilio__localidad__departamento__nombre__icontains=self.cleaned_data['departamento'])
				q3 = q3.filter(\
					extension_aulica__domicilio__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					extension_aulica__domicilio__localidad__departamento__nombre__icontains=self.cleaned_data['departamento'])
			if filter_by('localidad'):
				q1 = q1.filter(\
					establecimiento__domicilios__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					establecimiento__domicilios__localidad__nombre__icontains=self.cleaned_data['localidad'])
				q2 = q2.filter(\
					anexo__anexo_domicilio__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					anexo__anexo_domicilio__localidad__nombre__icontains=self.cleaned_data['localidad'])
				q3 = q3.filter(\
					extension_aulica__domicilio__tipo_domicilio__descripcion=EstablecimientoDomicilio.TIPO_INSTITUCIONAL, \
					extension_aulica__domicilio__localidad__nombre__icontains=self.cleaned_data['localidad'])

		q1.distinct().order_by('establecimiento__dependencia_funcional__jurisdiccion__nombre', 'establecimiento__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
		q2.distinct().order_by('anexo__dependencia_funcional__jurisdiccion__nombre', 'anexo__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
		q3.distinct().order_by('extension_aulica__dependencia_funcional__jurisdiccion__nombre', 'extension_aulica__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
		return [q1, q2, q3]
