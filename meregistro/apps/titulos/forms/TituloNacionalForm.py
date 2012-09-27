# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloNacional, EstadoTituloNacional, NormativaNacional, EstadoNormativaNacional


class TituloNacionalForm(forms.ModelForm):
	normativa_nacional = forms.ModelChoiceField(queryset=NormativaNacional.objects.filter(estado__nombre=EstadoNormativaNacional.VIGENTE).order_by('numero'), label='Normativa')
	observaciones = forms.CharField(widget=forms.Textarea, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoTituloNacional.objects.all().order_by('nombre'), required=False, empty_label=None)
	fecha_alta = forms.DateField(required=False, widget=forms.HiddenInput())

	class Meta:
		model = TituloNacional
		exclude = ('carreras')
