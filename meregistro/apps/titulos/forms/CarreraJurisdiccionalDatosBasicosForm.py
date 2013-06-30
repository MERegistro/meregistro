# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Carrera, CarreraJurisdiccional, EstadoCarrera
from apps.titulos.forms import CarreraJurisdiccionalForm


class CarreraJurisdiccionalDatosBasicosForm(forms.ModelForm):
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.order_by('nombre'), label='Nombre', required=True)
	
	class Meta:
	   model = CarreraJurisdiccional
	   fields = ('carrera',)

	def __init__(self, *args, **kwargs):
		self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
		super(CarreraJurisdiccionalDatosBasicosForm, self).__init__(*args, **kwargs)
		"Para no cargar quichicientosmil"
		self.fields['carrera'].queryset = self.fields['carrera'].queryset.filter(jurisdicciones__id=self.jurisdiccion_id, estado__nombre=EstadoCarrera.VIGENTE)


	def clean_carrera(self):
		c = self.cleaned_data['carrera']
		try:
			# chequeando si existe la combinación de carrera y jurisdicción
			ya_existe = CarreraJurisdiccional.objects\
				.filter(carrera=c, jurisdiccion__id=self.jurisdiccion_id)\
				.exclude(id=self.instance.id).exists()
			if ya_existe:
				raise ValidationError("Esta carrera ya se encuentra activa en su jurisdicción")
		except CarreraJurisdiccional.DoesNotExist:
			pass
		return c
