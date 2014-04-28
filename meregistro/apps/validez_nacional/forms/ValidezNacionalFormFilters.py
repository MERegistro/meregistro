# -*- coding: UTF-8 -*-

from django import forms
from apps.validez_nacional.models import ValidezNacional
from apps.registro.models import Establecimiento, Anexo, Jurisdiccion
from apps.titulos.models import Cohorte

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
class ValidezNacionalFormFilters(forms.Form):
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.all().order_by('nombre'), required=False)
	cue = forms.CharField(max_length=11, label='CUE', required=False)
	carrera = forms.CharField(max_length=40, label='Carrera', required=False)
	titulo_nacional = forms.CharField(max_length=40, label='Título', required=False)
	primera_cohorte = forms.ChoiceField(label='Primera Cohorte Autorizada', choices=ANIOS_COHORTE_CHOICES, required=False)
	nro_infd = forms.CharField(max_length=40, label='Número INFD', required=False)


	def __init__(self, *args, **kwargs):
		self.jur = kwargs.pop('jurisdiccion')
		super(ValidezNacionalFormFilters, self).__init__(*args, **kwargs)
		if self.jur:
			choices = [(j.id, j.nombre) for j in Jurisdiccion.objects.filter(pk=self.jur.id)]
			self.fields['jurisdiccion'] = forms.ChoiceField(choices=choices, required=False)
		
	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:			 
			q = ValidezNacional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if self.jur:
				from django.db.models import Q
				q = q.filter(
					(Q(tipo_unidad_educativa='Sede') & Q(unidad_educativa_id__in=[e.pk for e in Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=self.jur.id)])) |
					(Q(tipo_unidad_educativa='Anexo') & Q(unidad_educativa_id__in=[a.pk for a in Anexo.objects.filter(establecimiento__dependencia_funcional__jurisdiccion__id=self.jur.id)]))
				)
			else:
				if filter_by('jurisdiccion'):
					# Puede ser sede, anexo o jurisdicción, determinarlo
					from django.db.models import Q
					q = q.filter(
						(Q(tipo_unidad_educativa='Sede') & Q(unidad_educativa_id__in=[e.pk for e in Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=self.cleaned_data['jurisdiccion'].id)])) |
						(Q(tipo_unidad_educativa='Anexo') & Q(unidad_educativa_id__in=[a.pk for a in Anexo.objects.filter(establecimiento__dependencia_funcional__jurisdiccion__id=self.cleaned_data['jurisdiccion'].id)]))
					)
			if filter_by('cue'):
				q = q.filter(cue__icontains=self.cleaned_data['cue'])
			if filter_by('carrera'):
				q = q.filter(carrera__icontains=self.cleaned_data['carrera'])
			if filter_by('titulo_nacional'):
				q = q.filter(titulo_nacional__icontains=self.cleaned_data['titulo_nacional'])
			if filter_by('primera_cohorte'):
				q = q.filter(primera_cohorte=self.cleaned_data['primera_cohorte'])
			if filter_by('nro_infd'):
				q = q.filter(nro_infd__icontains=self.cleaned_data['nro_infd'])
		return q
