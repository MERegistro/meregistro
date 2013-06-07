# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import CarreraJurisdiccional, CarreraJurisdiccionalCohorte, Carrera, Cohorte, \
	EstadoCarreraJurisdiccional, TipoTitulo, \
	CohorteAnexo, EstadoCohorteAnexo, \
	CohorteEstablecimiento, EstadoCohorteEstablecimiento, \
	CohorteExtensionAulica, EstadoCohorteExtensionAulica
import datetime

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]

class CohortesUnidadEducativaFormFilters(forms.Form):

	anio = forms.ChoiceField(label='Año', choices=ANIOS_COHORTE_CHOICES, required=False)
	nombre_carrera = forms.CharField(max_length=40, label='Nombre de la Carrera', required=False)
	estado = forms.ModelChoiceField(queryset=None, required=False)
	
	
	def __init__(self, *args, **kwargs):
		self.tipo_unidad_educativa = kwargs.pop('tipo_unidad_educativa')
		super(CohortesUnidadEducativaFormFilters, self).__init__(*args, **kwargs)
		if self.tipo_unidad_educativa == 'establecimiento':
			self.fields['estado'].queryset = EstadoCohorteEstablecimiento.objects.all().order_by('nombre')
		elif self.tipo_unidad_educativa == 'anexo':
			self.fields['estado'].queryset = EstadoCohorteAnexo.objects.all().order_by('nombre')
		elif self.tipo_unidad_educativa == 'extension_aulica':
			self.fields['estado'].queryset = EstadoCohorteExtensionAulica.objects.all().order_by('nombre')


	def buildQuery(self, q=None):
		if self.tipo_unidad_educativa == 'establecimiento':
			filter_model = CohorteEstablecimiento
		elif self.tipo_unidad_educativa == 'anexo':
			filter_model = CohorteAnexo
		elif self.tipo_unidad_educativa == 'extension_aulica':
			filter_model = CohorteExtensionAulica
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = filter_model.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('anio'):
				q = q.filter(cohorte__anio=self.cleaned_data['anio'])
			if filter_by('nombre_carrera'):
				q = q.filter(cohorte__carrera_jurisdiccional__carrera__nombre__icontains=self.cleaned_data['nombre_carrera'])
			if filter_by('estado'):
				q = q.filter(estado=self.cleaned_data['estado'])
		q = q.order_by('cohorte__anio', 'cohorte__carrera_jurisdiccional__carrera__nombre')
		return q.filter(oferta__exact=True)
