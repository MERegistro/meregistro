# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import PostituloNacional, EstadoPostituloNacional, NormativaPostitulo, EstadoNormativaPostitulo


class PostituloNacionalForm(forms.ModelForm):
	nombre = forms.CharField(max_length=255, required=True)
	normativa_postitulo = forms.ModelChoiceField(queryset=NormativaPostitulo.objects.filter(estado__nombre=EstadoNormativaPostitulo.VIGENTE).order_by('numero'), label='Normativa')
	observaciones = forms.CharField(widget=forms.Textarea, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoPostituloNacional.objects.all().order_by('nombre'), required=False, empty_label=None)
	fecha_alta = forms.DateField(required=False, widget=forms.HiddenInput())

	class Meta:
		model = PostituloNacional
		exclude = ('carreras')
