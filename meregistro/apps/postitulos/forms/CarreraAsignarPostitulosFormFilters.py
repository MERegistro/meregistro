# -*- coding: UTF-8 -*-

from django import forms
from apps.postitulos.models import PostituloNacional, EstadoPostituloNacional, NormativaPostitulo, EstadoNormativaPostitulo


class CarreraAsignarPostitulosFormFilters(forms.Form):
	# 394
	# normativa_nacional = forms.ModelChoiceField(queryset=NormativaNacional.objects.filter(estado__nombre=EstadoNormativaNacional.VIGENTE).order_by('numero'), label='Normativa', required=False)
	normativa_postitulo = forms.ModelChoiceField(queryset=NormativaPostitulo.objects.all().order_by('numero'), label='Normativa', required=False)

	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = PostituloNacional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('normativa_postitulo'):
				q = q.filter(normativa_postitulo=self.cleaned_data['normativa_postitulo'])
			
		return q.filter(estado__nombre=EstadoPostituloNacional.VIGENTE)
