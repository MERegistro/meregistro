# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import ValidezNacional
from apps.postitulos.models import CohortePostitulo


ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(CohortePostitulo.PRIMER_ANIO, CohortePostitulo.ULTIMO_ANIO)]
class ValidezNacionalForm(forms.ModelForm):
	cue = forms.CharField(max_length=9, label='CUE', required=True)
	carrera_postitulo = forms.CharField(max_length=255, label='Carrera', required=True)
	postitulo_nacional = forms.CharField(max_length=255, label='Postítulo', required=True)
	primera_cohorte = forms.ChoiceField(label='Primera Cohorte Autorizada', choices=ANIOS_COHORTE_CHOICES, required=True)
	ultima_cohorte = forms.ChoiceField(label='Última Cohorte Autorizada', choices=ANIOS_COHORTE_CHOICES, required=True)
	normativa_postitulo_jurisdiccional = forms.CharField(max_length=255, label='Normativa Jurisdiccional', required=True)
	normativas_postitulo = forms.CharField(max_length=255, label='Normativa Nacional', required=True)
	nro_infd = forms.CharField(max_length=255, label='Nro. INFD.', required=True)
	
	class Meta:
	   model = ValidezNacional
	   fields = ('cue', 'carrera_postitulo', 'postitulo_nacional', 'primera_cohorte', 'ultima_cohorte', 'normativa_postitulo_jurisdiccional', 'normativas_postitulo', 'nro_infd')

	def __init__(self, *args, **kwargs):
		super(ValidezNacionalForm, self).__init__(*args, **kwargs)

