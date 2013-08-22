# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Cohorte, CohorteEstablecimiento, CohorteEstablecimientoSeguimiento


ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]

class CohorteEstablecimientoSeguimientoForm(forms.ModelForm):
	anio = forms.ChoiceField(label='Año', required=True, choices=ANIOS_COHORTE_CHOICES)
	observaciones = forms.CharField(widget=forms.Textarea, required=False)

	class Meta:
		model = CohorteEstablecimientoSeguimiento

	"Le agrego el inscriptos_total para chequear la suma"
	def __init__(self, *args, **kwargs):
		self.cohorte_establecimiento = kwargs.pop('cohorte_unidad_educativa')
		super(CohorteEstablecimientoSeguimientoForm, self).__init__(*args, **kwargs)
		self.fields["cohorte_establecimiento"].initial = self.cohorte_establecimiento
		
		" Si lo estoy creando, sólo puedo cargar el año siguiente "
		if not self.instance.id:
			ultimo_seguimiento_cargado = self.cohorte_establecimiento.get_ultimo_seguimiento_cargado()
			if len(ultimo_seguimiento_cargado) > 0: # Tiene años previos cargados?
				self.fields["anio"].choices = [(ultimo_seguimiento_cargado.get().anio + 1, ultimo_seguimiento_cargado.get().anio + 1)]
			else: # Cargar el primero disponible
				self.fields["anio"].choices = [(self.cohorte_establecimiento.cohorte.anio + 1, self.cohorte_establecimiento.cohorte.anio + 1)]
		else: # Se está editando
			self.fields["anio"].choices = [(self.instance.anio, self.instance.anio)]


	def clean(self):
		self.cleaned_data['cohorte_establecimiento'] = self.cohorte_establecimiento
		try:
			solo_cursan_nuevas_unidades = int(self.cleaned_data['solo_cursan_nuevas_unidades'])
			no_cursan = int(self.cleaned_data['no_cursan'])
			recursan_cursan_nuevas_unidades = int(self.cleaned_data['recursan_cursan_nuevas_unidades'])
			solo_recursan_nuevas_unidades = int(self.cleaned_data['solo_recursan_nuevas_unidades'])
			" Si se está editando, no contar todos los egresados "
			if self.instance.id:
				egresados_total = self.cohorte_establecimiento.get_total_egresados() - self.instance.egresados + self.cleaned_data['egresados']
			else:
				egresados_total = self.cohorte_establecimiento.get_total_egresados() + self.cleaned_data['egresados']
			
			if solo_cursan_nuevas_unidades + no_cursan + recursan_cursan_nuevas_unidades + solo_recursan_nuevas_unidades + egresados_total  != self.cohorte_establecimiento.inscriptos:
				raise ValidationError('La suma de los que cursan nuevas unidades, los que sólo recursan, los que están cursando ambas opciones y los que no cursan ninguna unidad curricular debe ser igual a ' + str(self.cohorte_establecimiento.inscriptos - egresados_total) + ', la cantidad total de inscriptos en los profesorados en primer año de la cohorte correspondiente menos los egresados que haya habido hasta el momento (incluyendo los que se están cargando ahora).')
		except KeyError:
			pass
		return self.cleaned_data


	def clean_anio(self):
		cohorte_establecimiento_id = self.cohorte_establecimiento.id
		try:
			registro = CohorteEstablecimientoSeguimiento.objects.get(cohorte_establecimiento=cohorte_establecimiento_id, anio=self.cleaned_data['anio'])
		except:
			registro = None
		if registro is not None and registro.id != self.instance.id:
			raise ValidationError("Ya se realiza el seguimiento para este año")
		return self.cleaned_data['anio']
