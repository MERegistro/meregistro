# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from apps.titulos.models import Carrera, EstadoCarrera
from apps.registro.models import Jurisdiccion
import datetime

class CarreraForm(ModelForm):
	nombre = forms.CharField(max_length=100, required=True)
	jurisdicciones = forms.ModelMultipleChoiceField(queryset=Jurisdiccion.objects.all().order_by('nombre'), widget=forms.CheckboxSelectMultiple)
	observaciones = forms.CharField(widget=forms.Textarea, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoCarrera.objects.all().order_by('nombre'), required=True, empty_label=None)
	fecha_alta = forms.DateField(required=False, widget=forms.HiddenInput())
    
	class Meta:
		model = Carrera

	def clean(self):
		cleaned = super(CarreraForm, self).clean()
		if len(self.errors) == 0 and self.cleaned_data['nombre'] != '':
			q = Carrera.objects.filter(nombre__iexact=self.cleaned_data['nombre']).exclude(id=self.instance.id)
			if len(q) > 0:
				raise forms.ValidationError("La carrera ya se encuentra registrada")
		return cleaned
