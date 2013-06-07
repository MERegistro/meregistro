# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Cohorte
from apps.validez_nacional.models import Solicitud

COHORTES_SOLICITADAS_CHOICES = [('', '-------')] + [(i, i) for i in range(1, 6)]
PRIMERA_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]
ULTIMA_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO + 5)]

class SolicitudCohortesForm(forms.ModelForm):
	cohortes_solicitadas = forms.ChoiceField(label='Duración', choices=COHORTES_SOLICITADAS_CHOICES, required=True)
	primera_cohorte = forms.ChoiceField(label='Primera cohorte', choices=PRIMERA_COHORTE_CHOICES, required=True)
	ultima_cohorte = forms.ChoiceField(label='Última cohorte', choices=ULTIMA_COHORTE_CHOICES, required=True)
	
	class Meta:
	   model = Solicitud
	   fields = ('primera_cohorte', 'ultima_cohorte',)

	def __init__(self, *args, **kwargs):
		super(SolicitudCohortesForm, self).__init__(*args, **kwargs)
	
