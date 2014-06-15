# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import CarreraPostitulo, CarreraPostituloJurisdiccional, EstadoCarreraPostitulo


class CarreraPostituloJurisdiccionalDatosBasicosForm(forms.ModelForm):
	carrera_postitulo = forms.ModelChoiceField(queryset=CarreraPostitulo.objects.order_by('nombre'), label='Nombre', required=True)
	
	class Meta:
	   model = CarreraPostituloJurisdiccional
	   fields = ('carrera_postitulo',)

	def __init__(self, *args, **kwargs):
		self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
		super(CarreraPostituloJurisdiccionalDatosBasicosForm, self).__init__(*args, **kwargs)
		"Para no cargar quichicientosmil"
		self.fields['carrera_postitulo'].queryset = self.fields['carrera_postitulo'].queryset.filter(jurisdicciones__id=self.jurisdiccion_id, estado__nombre=EstadoCarreraPostitulo.VIGENTE)


	def clean_carrera_postitulo(self):
		c = self.cleaned_data['carrera_postitulo']
		try:
			# chequeando si existe la combinación de carrera y jurisdicción
			ya_existe = CarreraPostituloJurisdiccional.objects\
				.filter(carrera_postitulo=c, jurisdiccion__id=self.jurisdiccion_id)\
				.exclude(id=self.instance.id).exists()
			if ya_existe:
				raise ValidationError("Esta carrera ya se encuentra activa en su jurisdicción")
		except CarreraPostituloJurisdiccional.DoesNotExist:
			pass
		return c
