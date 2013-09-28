# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Establecimiento, Anexo, EstadoEstablecimiento, EstadoAnexo

class SolicitudAsignacionFormFilters(forms.Form):
	cue = forms.CharField(max_length=11, label='CUE', required=False)
	unidad_educativa = forms.CharField(max_length=40, label='Unidad Educativa', required=False)


	def __init__(self, *args, **kwargs):
		self.tipo_ue = kwargs.pop('tipo_ue')
		self.solicitud = kwargs.pop('solicitud')
		super(SolicitudAsignacionFormFilters, self).__init__(*args, **kwargs)
		
		
	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			if self.tipo_ue == 'Establecimiento':
				q = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=self.solicitud.jurisdiccion_id, estado__nombre=EstadoEstablecimiento.REGISTRADO)
			else: 
				q = Anexo.objects.filter(establecimiento__dependencia_funcional__jurisdiccion__id=self.solicitud.jurisdiccion_id, estado__nombre=EstadoAnexo.REGISTRADO)		
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('cue'):
				q = q.filter(cue__icontains=self.cleaned_data['cue'])
			if filter_by('unidad_educativa'):
				q = q.filter(nombre__icontains=self.cleaned_data['unidad_educativa'])
		return q
