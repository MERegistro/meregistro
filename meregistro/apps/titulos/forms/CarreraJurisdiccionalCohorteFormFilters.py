# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import CarreraJurisdiccional, CarreraJurisdiccionalCohorte, Carrera, EstadoCarreraJurisdiccional, Cohorte	
import datetime

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
	
class CarreraJurisdiccionalCohorteFormFilters(forms.Form):

	carrera = forms.CharField(max_length=40, label='Carrera', required=False)
	anio_cohorte_autorizada = forms.ChoiceField(label='Cohorte autorizada', choices=ANIOS_COHORTE_CHOICES, required=False)
	anio_cohorte_generada = forms.ChoiceField(label='Cohorte generada', choices=ANIOS_COHORTE_CHOICES, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoCarreraJurisdiccional.objects.all().order_by('nombre'), required=False)

	def buildQuery(self, q = None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = CarreraJurisdiccional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('carrera'):
				q = q.filter(carrera__nombre__icontains = self.cleaned_data['carrera'])
			if filter_by('anio_cohorte_autorizada'):
				q = q.filter(datos_cohorte__ultima_cohorte_autorizada__lte=self.cleaned_data['anio_cohorte_autorizada'], datos_cohorte__primera_cohorte_autorizada__gte=self.cleaned_data['anio_cohorte_autorizada'])
			if filter_by('anio_cohorte_generada'):
				q = q.filter(cohortes__anio=self.cleaned_data['anio_cohorte_generada'])
			if filter_by('estado'):
				q = q.filter(estado=self.cleaned_data['estado'])
		q = q.order_by('carrera__nombre')
		return q
