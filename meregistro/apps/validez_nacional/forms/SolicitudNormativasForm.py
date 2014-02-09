# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import NormativaJurisdiccional
from apps.validez_nacional.models import Solicitud


class SolicitudNormativasForm(forms.ModelForm):
    normativas_jurisdiccionales = forms.ModelMultipleChoiceField(queryset=NormativaJurisdiccional.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
       model = Solicitud
       fields = ('normativas_jurisdiccionales',)

