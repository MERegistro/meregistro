# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from apps.titulos.models import Carrera, EstadoCarrera
from apps.registro.models import Jurisdiccion
import datetime

class CarreraForm(ModelForm):
	jurisdicciones = forms.ModelMultipleChoiceField(queryset=Jurisdiccion.objects.all().order_by('nombre'), widget=forms.CheckboxSelectMultiple)
	observaciones = forms.CharField(widget=forms.Textarea, required=False)
	estado = forms.ModelChoiceField(queryset=EstadoCarrera.objects.all().order_by('nombre'), required=True, empty_label=None)
	fecha_alta = forms.DateField(required=False, widget=forms.HiddenInput())
    
	class Meta:
		model = Carrera

