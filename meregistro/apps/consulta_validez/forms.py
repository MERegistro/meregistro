# -*- coding: UTF-8 -*-

"""
from django import forms
from apps.registro.models import Jurisdiccion, TipoGestion
from apps.consulta_validez.models import UnidadEducativa, Titulo
"""

from django import forms
from apps.validez_nacional.models import ValidezNacional
from apps.registro.models import Establecimiento, Anexo, Jurisdiccion, TipoGestion
from apps.titulos.models import Cohorte, Carrera, TituloNacional
from itertools import chain

sedes = Establecimiento.objects.order_by('cue').values_list('id', 'cue', 'nombre')
anexos = Anexo.objects.order_by('cue').values_list('id', 'cue', 'nombre')
unidades_educativas = [('', '---------')] + [(ue[0], ue[1] + " - " + ue[2]) for ue in list(chain(sedes, anexos))]

titulos = TituloNacional.objects.order_by('nombre').values_list('nombre')
titulos = [('', '---------')] + [(t[0], t[0]) for t in titulos.distinct('nombre')]

class ConsultaValidezFormFilters(forms.Form):
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdiccion', required=False)
	tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.order_by('nombre'), label='Tipo de Gestión', required=False)
	cue = forms.CharField(max_length=40, label='Cue', required=False)
	unidad_educativa = forms.ChoiceField(choices=unidades_educativas, label='Nombre del ISFD', required=False)
	carrera = forms.CharField(max_length=50, label='Carrera', required=False)
	titulo = forms.CharField(max_length=50, label='Título', required=False)
	cohorte = forms.CharField(max_length=4, label='Cohorte', required=False)
	nroinfd = forms.CharField(label='Número de INFD', required=False)
	
	
	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = ValidezNacional.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
				
			if filter_by('jurisdiccion'):
				# Puede ser sede o anexo, determinarlo según tipo_unidad_educativa
				from django.db.models import Q
				q = q.filter(
					(Q(tipo_unidad_educativa='Sede') & Q(unidad_educativa_id__in=[e.pk for e in Establecimiento.objects.filter(dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])])) |
					(Q(tipo_unidad_educativa='Anexo') & Q(unidad_educativa_id__in=[a.pk for a in Anexo.objects.filter(establecimiento__dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])]))
				)
			if filter_by('tipo_gestion'):
				# Puede ser sede o anexo, determinarlo según tipo_unidad_educativa
				from django.db.models import Q
				q = q.filter(
					(Q(tipo_unidad_educativa='Sede') & Q(unidad_educativa_id__in=[e.pk for e in Establecimiento.objects.filter(dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])])) |
					(Q(tipo_unidad_educativa='Anexo') & Q(unidad_educativa_id__in=[a.pk for a in Anexo.objects.filter(establecimiento__dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])]))
				)
			if filter_by('cue'):
				q = q.filter(cue__icontains=self.cleaned_data['cue'])
			if filter_by('unidad_educativa'):
				# Puede ser sede o anexo, determinarlo según tipo_unidad_educativa
				from django.db.models import Q
				q = q.filter(
					(Q(tipo_unidad_educativa='Sede') & Q(unidad_educativa_id__in=[e.pk for e in Establecimiento.objects.filter(pk=self.cleaned_data['unidad_educativa'])])) |
					(Q(tipo_unidad_educativa='Anexo') & Q(unidad_educativa_id__in=[a.pk for a in Anexo.objects.filter(pk=self.cleaned_data['unidad_educativa'])]))
				)
			if filter_by('carrera'):
				q = q.filter(carrera__icontains=self.cleaned_data['carrera'])
			if filter_by('titulo'):
				q = q.filter(titulo_nacional__icontains=self.cleaned_data['titulo'])
			if filter_by('cohorte'):
				q = q.filter(primera_cohorte__lte=self.cleaned_data['cohorte'], ultima_cohorte__gte=self.cleaned_data['cohorte'])
			if filter_by('nroinfd'):
				q = q.filter(nro_infd__icontains=self.cleaned_data['nroinfd'].strip())
		
		return q
