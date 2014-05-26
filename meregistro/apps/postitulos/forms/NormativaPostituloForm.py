# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import NormativaPostitulo, EstadoNormativaPostitulo


class NormativaPostituloForm(forms.ModelForm):
	observaciones = forms.CharField(widget=forms.Textarea, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoNormativaPostitulo.objects.all().order_by('nombre'), required=True, empty_label=None)
	fecha_alta = forms.DateField(required=False, widget=forms.HiddenInput())

	class Meta:
		model = NormativaPostitulo
