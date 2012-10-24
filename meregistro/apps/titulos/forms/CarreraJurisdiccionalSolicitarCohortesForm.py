# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import CarreraJurisdiccionalCohorte
import datetime


class CarreraJurisdiccionalSolicitarCohortesForm(forms.ModelForm):

    COHORTES_SOLICITADAS_CHOICES = [('', '-------')] + [(i, i) for i in range(1, 6)]
    PRIMERA_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(2000, 2021)]
    ULTIMA_COHORTE_CHOICES = [('', '-------')] + [(i, i) for i in range(2000, 2031)]
    cohortes_aprobadas = forms.ChoiceField(label='Duración', choices=COHORTES_SOLICITADAS_CHOICES, required=True)
    primera_cohorte_solicitada = forms.ChoiceField(label='Año primera cohorte', choices=PRIMERA_COHORTE_CHOICES, required=True)
    ultima_cohorte_solicitada = forms.ChoiceField(label='Año última cohorte', choices=ULTIMA_COHORTE_CHOICES, required=True)
    observaciones = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = CarreraJurisdiccionalCohorte
        exclude = ('carrera_jurisdiccional', 'primera_cohorte_autorizada', 'ultima_cohorte_autorizada')

    def clean(self):
        cleaned_data = self.cleaned_data
        return cleaned_data

    def clean_anio_ultima_cohorte(self):
        cleaned_data = self.cleaned_data
        if cleaned_data['ultima_cohorte_solicitada'] < cleaned_data['primera_cohorte_solicitada']:
            raise ValidationError(u'El año de la última cohorte no puede ser menor al de inicio de cohorte.')
        return cleaned_data['anio_ultima_cohorte']
