# -*- coding: UTF-8 -*-

from django import forms
from apps.validez_nacional.models import SolicitudEstablecimiento, SolicitudAnexo

class SolicitudInstitucionalFormFilters(forms.Form):

	def __init__(self, *args, **kwargs):
		self.ambito = kwargs.pop('ambito')
		super(SolicitudInstitucionalFormFilters, self).__init__(*args, **kwargs)
        
        
	def buildQuery(self, q=None):
		from itertools import chain
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = list(chain(SolicitudEstablecimiento.objects.filter(establecimiento__ambito__path__istartswith=self.ambito.path), SolicitudAnexo.objects.filter(anexo__establecimiento__ambito__path__istartswith=self.ambito.path)))
			#q = list(chain(SolicitudEstablecimiento.objects.all(), SolicitudAnexo.objects.filter()))
		return q
