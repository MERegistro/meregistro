# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.validez_nacional.models import ValidezNacional
from apps.titulos.models import Cohorte


ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
class ValidezNacionalForm(forms.ModelForm):
	cue = forms.CharField(max_length=9, label='CUE', required=True)
	carrera = forms.CharField(max_length=255, label='Carrera', required=True)
	titulo_nacional = forms.CharField(max_length=255, label='Título', required=True)
	primera_cohorte = forms.ChoiceField(label='Primera Cohorte Autorizada', choices=ANIOS_COHORTE_CHOICES, required=True)
	ultima_cohorte = forms.ChoiceField(label='Última Cohorte Autorizada', choices=ANIOS_COHORTE_CHOICES, required=True)
	normativa_jurisdiccional = forms.CharField(max_length=255, label='Normativa Jurisdiccional', required=True)
	dictamen_cofev = forms.CharField(max_length=255, label='Dictamen CoFEv', required=True)
	normativas_nacionales = forms.CharField(max_length=255, label='Normativa Nacional', required=True)
	nro_infd = forms.CharField(max_length=255, label='Nro. INFD.', required=True)
	
	class Meta:
	   model = ValidezNacional
	   fields = ('cue', 'carrera', 'titulo_nacional', 'primera_cohorte', 'ultima_cohorte', 'normativa_jurisdiccional', 'dictamen_cofev', 'normativas_nacionales', 'nro_infd')

	def __init__(self, *args, **kwargs):
		super(ValidezNacionalForm, self).__init__(*args, **kwargs)

