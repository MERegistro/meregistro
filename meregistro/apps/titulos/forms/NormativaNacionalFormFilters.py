# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import NormativaNacional, EstadoNormativaNacional


class NormativaNacionalFormFilters(forms.Form):
	numero = forms.CharField(max_length=50, label='Número', required=False)
	descripcion = forms.CharField(max_length=50, label='Descripción', required=False)
	estado = forms.ModelChoiceField(queryset=EstadoNormativaNacional.objects.all().order_by('nombre'), required=False)


	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = NormativaNacional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
		if filter_by('numero'):
			q = q.filter(numero__icontains=self.cleaned_data['numero'])
		if filter_by('descripcion'):
			q = q.filter(descripcion__icontains=self.cleaned_data['descripcion'])
		if filter_by('estado'):
			q = q.filter(estado=self.cleaned_data['estado'])
		return q
