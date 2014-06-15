# -*- coding: UTF-8 -*-

from django import forms
from apps.postitulos.models import CarreraPostitulo, EstadoCarreraPostitulo
from apps.registro.models import Jurisdiccion

class CarreraPostituloFormFilters(forms.Form):
	nombre = forms.CharField(max_length=40, label='Nombre', required=False)
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdicción', required=False)
	estado = forms.ModelChoiceField(queryset=EstadoCarreraPostitulo.objects.all().order_by('nombre'), required=False)
	
	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = CarreraPostitulo.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
		if filter_by('nombre'):
			q = q.filter(nombre__icontains=self.cleaned_data['nombre'])
		if filter_by('jurisdiccion'):
			q = q.filter(jurisdicciones__id=self.cleaned_data['jurisdiccion'].id)
		if filter_by('estado'):
			q = q.filter(estado=self.cleaned_data['estado'])
		return q
