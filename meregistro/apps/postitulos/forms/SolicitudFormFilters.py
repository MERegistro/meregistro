# -*- coding: UTF-8 -*-

from django import forms
from apps.postitulos.models import Solicitud, EstadoSolicitud, CohortePostitulo, CarreraPostitulo
from apps.registro.models import Jurisdiccion
from django.db.models import Min, Max

primera_cohorte = Solicitud.objects.all().aggregate(Min('primera_cohorte'))['primera_cohorte__min']
ultima_primera_cohorte = Solicitud.objects.all().aggregate(Max('primera_cohorte'))['primera_cohorte__max']

if primera_cohorte is None:
	primera_cohorte = CohortePostitulo.PRIMER_ANIO
if ultima_primera_cohorte is None:
	ultima_primera_cohorte = CohortePostitulo.ULTIMO_ANIO

ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(primera_cohorte, ultima_primera_cohorte+1)]

class SolicitudFormFilters(forms.Form):

	postitulo = forms.CharField(max_length=40, label='Título', required=False)
	primera_cohorte = forms.ChoiceField(label='Cohorte', choices=ANIOS_COHORTE_CHOICES, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoSolicitud.objects.all().order_by('nombre'), required=False)
	jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.all().order_by('nombre'), required=False)
	carrera_postitulo = forms.CharField(max_length=40, label='Carrera', required=False)
	normativa_postitulo = forms.CharField(max_length=40, label='Normativa Nacional', required=False)
	nro_expediente = forms.CharField(max_length=40, label='Nro. de Expediente', required=False)

	def buildQuery(self, q=None):
		"""
		Crea o refina un query de búsqueda.
		"""
		if q is None:
			q = Solicitud.objects.all()
		if self.is_valid():
			def filter_by(field):
				return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
		if filter_by('titulo'):
			q = q.filter(titulo_nacional__nombre__icontains=self.cleaned_data['titulo'])
		if filter_by('carrera_postitulo'):
			q = q.filter(carrera_postitulo__nombre__icontains=self.cleaned_data['carrera_postitulo'])
		if filter_by('primera_cohorte'):
			q = q.filter(primera_cohorte=self.cleaned_data['primera_cohorte'])
		if filter_by('estado'):
			q = q.filter(estado=self.cleaned_data['estado'])
		if filter_by('jurisdiccion'):
			q = q.filter(jurisdiccion=self.cleaned_data['jurisdiccion'])
		if filter_by('normativa_nacional'):
			q = q.filter(normativas_nacionales__icontains=self.cleaned_data['normativa_postitulo'])
		if filter_by('nro_expediente'):
			q = q.filter(nro_expediente__icontains=self.cleaned_data['nro_expediente'])
		return q
