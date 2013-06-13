# -*- coding: UTF-8 -*-

from django import forms
from apps.validez_nacional.models import ValidezNacional
from apps.registro.models import Establecimiento

class ValidezInstitucionalFormFilters(forms.Form):

	def __init__(self, *args, **kwargs):
		self.establecimiento = kwargs.pop('establecimiento')
		super(ValidezInstitucionalFormFilters, self).__init__(*args, **kwargs)
        
        
	def buildQuery(self, q=None):
		from itertools import chain
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:			 
			q = ValidezNacional.objects.filter(tipo_unidad_educativa=ValidezNacional.TIPO_UE_SEDE, unidad_educativa_id=self.establecimiento.id) \
			| ValidezNacional.objects.filter(tipo_unidad_educativa=ValidezNacional.TIPO_UE_ANEXO,unidad_educativa_id__in=[a.id for a in self.establecimiento.anexos.all()])
		return q
