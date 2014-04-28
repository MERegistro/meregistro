# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import TituloNacional, EstadoTituloNacional, NormativaNacional, EstadoNormativaNacional


class CarreraAsignarTitulosFormFilters(forms.Form):
	# 394
	# normativa_nacional = forms.ModelChoiceField(queryset=NormativaNacional.objects.filter(estado__nombre=EstadoNormativaNacional.VIGENTE).order_by('numero'), label='Normativa', required=False)
	normativa_nacional = forms.ModelChoiceField(queryset=NormativaNacional.objects.all().order_by('numero'), label='Normativa', required=False)

	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = TituloNacional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('normativa_nacional'):
				q = q.filter(normativa_nacional=self.cleaned_data['normativa_nacional'])
			
		return q.filter(estado__nombre=EstadoTituloNacional.VIGENTE)
