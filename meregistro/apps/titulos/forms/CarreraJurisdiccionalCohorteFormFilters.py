# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import CarreraJurisdiccional, CarreraJurisdiccionalCohorte, Carrera, EstadoCarreraJurisdiccional, Cohorte
from apps.registro.models import Jurisdiccion
import datetime

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
	
class CarreraJurisdiccionalCohorteFormFilters(forms.Form):

	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.all().order_by('nombre'), required=False)
	carrera = forms.CharField(max_length=40, label='Carrera', required=False)
	anio_cohorte_solicitada = forms.ChoiceField(label='Cohorte solicitada', choices=ANIOS_COHORTE_CHOICES, required=False)
	anio_cohorte_generada = forms.ChoiceField(label='Cohorte generada', choices=ANIOS_COHORTE_CHOICES, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoCarreraJurisdiccional.objects.all().order_by('nombre'), required=False)
	
	def __init__(self, *args, **kwargs):
		self.jur = kwargs.pop('jurisdiccion')
		super(CarreraJurisdiccionalCohorteFormFilters, self).__init__(*args, **kwargs)
		if self.jur:
			choices = [(j.id, j.nombre) for j in Jurisdiccion.objects.filter(pk=self.jur.id)]
			self.fields['jurisdiccion'] = forms.ChoiceField(choices=choices, required=False)


	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = CarreraJurisdiccional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if self.jur:
				q = q.filter(jurisdiccion=self.jur)
			else:
				if filter_by('jurisdiccion'):
					q = q.filter(jurisdiccion=self.cleaned_data['jurisdiccion'])
			if filter_by('carrera'):
				q = q.filter(carrera__nombre__icontains = self.cleaned_data['carrera'])
			if filter_by('anio_cohorte_solicitada'):
				q = q.filter(datos_cohorte__ultima_cohorte_solicitada__lte=self.cleaned_data['anio_cohorte_solicitada'], datos_cohorte__primera_cohorte_solicitada__gte=self.cleaned_data['anio_cohorte_solicitada'])
			if filter_by('anio_cohorte_generada'):
				q = q.filter(cohortes__anio=self.cleaned_data['anio_cohorte_generada'])
			if filter_by('estado'):
				q = q.filter(estado=self.cleaned_data['estado'])

		q = q.order_by('carrera__nombre')
		return q
