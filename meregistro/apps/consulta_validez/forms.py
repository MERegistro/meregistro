# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Jurisdiccion
from apps.consulta_validez.models import UnidadEducativa, Titulo

class TitulosChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.denominacion

class CarrerasChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.carrera

class ConsultaValidezFormFilters(forms.Form):
	
	jur_choices = [[i, j] for i,j in Jurisdiccion.objects.order_by('nombre').values_list('id', 'nombre')]
	ue_choices = [[i, c+' - '+n] for i,c,n in UnidadEducativa.objects.all().order_by('nombre').values_list('id', 'cue', 'nombre')]
	carrera_choices = [[i, c] for i,c in Titulo.objects.order_by('carrera').distinct('carrera').values_list('id', 'carrera')]
	titulo_choices = [[i, d] for i,d in Titulo.objects.order_by('denominacion').distinct('denominacion').values_list('id', 'denominacion')]

	jurisdiccion = forms.ChoiceField(choices=[['', '--------']] + jur_choices, label='Jurisdiccion', required=False)
	cue = forms.CharField(max_length=40, label='Cue', required=False)
	unidad_educativa = forms.ChoiceField(choices=[['0', '--------']] + ue_choices, label='Nombre del ISFD', required=False)
	carrera = forms.ChoiceField(choices=[['0', '--------']] + carrera_choices, label='Carrera', required=False)
	titulo = forms.ChoiceField(choices=[['0', '--------']] + titulo_choices, label='Título', required=False)
	#carrera = CarrerasChoiceField(queryset=Titulo.objects.order_by('carrera').distinct('carrera'), label='Carrera', required=False)
	#titulo = TitulosChoiceField(queryset=Titulo.objects.order_by('denominacion').distinct('denominacion'), label='Título', required=False)
	cohorte = forms.CharField(max_length=4, label='Cohorte', required=False)
	
	
	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = Titulo.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
			if filter_by('jurisdiccion'):
				q = q.filter(unidad_educativa__jurisdiccion=self.cleaned_data['jurisdiccion'])
			if filter_by('cue'):
				q = q.filter(unidad_educativa__cue=self.cleaned_data['cue'])
			if filter_by('unidad_educativa') and self.cleaned_data['unidad_educativa'] != '0':
				q = q.filter(unidad_educativa=self.cleaned_data['unidad_educativa'])
			if filter_by('carrera') and self.cleaned_data['carrera'] != '0':
				q = q.filter(carrera=Titulo.objects.get(pk=self.cleaned_data['carrera']).carrera)
			if filter_by('titulo') and self.cleaned_data['titulo'] != '0':
				q = q.filter(denominacion=Titulo.objects.get(pk=self.cleaned_data['titulo']).denominacion)
			if filter_by('cohorte'):
				q = q.filter(primera__lte=self.cleaned_data['cohorte'], ultima__gte=self.cleaned_data['cohorte'])
		return q
