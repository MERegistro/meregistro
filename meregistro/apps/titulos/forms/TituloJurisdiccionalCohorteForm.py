# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccionalCohorte
import datetime


class TituloJurisdiccionalCohorteForm(forms.ModelForm):

    COHORTES_APROBADAS_CHOICES = [('', '-------')] + [(i, i) for i in range(1, 6)]
    ANIOS_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(2000, 2021)]
    cohortes_aprobadas = forms.ChoiceField(label = 'Duración', choices = COHORTES_APROBADAS_CHOICES, required = True)
    anio_primera_cohorte = forms.ChoiceField(label = 'Año primera cohorte', choices = ANIOS_COHORTE_CHOICES, required = True)
    anio_ultima_cohorte = forms.ChoiceField(label = 'Año última cohorte', choices = ANIOS_COHORTE_CHOICES, required = True)
    observaciones = forms.CharField(widget = forms.Textarea, required = False)

    class Meta:
        model = TituloJurisdiccionalCohorte
        exclude = ('titulo_jurisdiccional',)

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def clean_anio_ultima_cohorte(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['anio_ultima_cohorte'] < cleaned_data['anio_primera_cohorte']:
            raise ValidationError(u'El año de la última cohorte no puede ser menor al de inicio de cohorte.')
        return cleaned_data['anio_ultima_cohorte']
