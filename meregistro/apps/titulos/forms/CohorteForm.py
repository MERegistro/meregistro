# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Cohorte



class CohorteForm(forms.ModelForm):

	ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(Cohorte.PRIMER_ANIO, Cohorte.ULTIMO_ANIO)]

	anio = forms.ChoiceField(label='Año', choices=ANIOS_COHORTE_CHOICES, required=True)
	observaciones = forms.CharField(widget = forms.Textarea, required = False)

	class Meta:
		model = Cohorte
		exclude = ('establecimientos', 'anexos', 'extensiones_aulicas',)
