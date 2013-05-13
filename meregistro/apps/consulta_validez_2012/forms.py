# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Jurisdiccion, TipoGestion
from apps.consulta_validez_2012.models import UnidadEducativa, Titulo




class ConsultaValidezFormFilters(forms.Form):
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdiccion', required=False)
	tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.order_by('nombre'), label='Tipo de Gestión', required=False)
	cue = forms.CharField(max_length=40, label='Cue', required=False)
	unidad_educativa = forms.ModelChoiceField(queryset=UnidadEducativa.objects.order_by('nombre'), label='Nombre del ISFD', required=False)
	carrera = forms.ChoiceField(label='Carrera', required=False)
	titulo = forms.ChoiceField(label='Título', required=False)
	cohorte = forms.CharField(max_length=4, label='Cohorte', required=False)
	nroinfd = forms.CharField(label='Número de INFD', required=False)
	
	
	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = Titulo.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('jurisdiccion'):
				q = q.filter(unidad_educativa__jurisdiccion=self.cleaned_data['jurisdiccion'])
			if filter_by('tipo_gestion'):
				q = q.filter(unidad_educativa__dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])
			if filter_by('cue'):
				q = q.filter(unidad_educativa__cue=self.cleaned_data['cue'])
			if filter_by('unidad_educativa'):
				q = q.filter(unidad_educativa=self.cleaned_data['unidad_educativa'])
			if filter_by('carrera'):
				q = q.filter(carrera=self.cleaned_data['carrera'])
			if filter_by('nroinfd'):
				q = q.filter(nroinfd=self.cleaned_data['nroinfd'].strip())
			if filter_by('titulo'):
				q = q.filter(denominacion=self.cleaned_data['titulo'])
			if filter_by('cohorte'):
				q = q.filter(primera__lte=self.cleaned_data['cohorte'], ultima__gte=self.cleaned_data['cohorte'])
		return q.distinct()
