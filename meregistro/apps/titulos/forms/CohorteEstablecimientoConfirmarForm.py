# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import CohorteEstablecimiento


class CohorteEstablecimientoConfirmarForm(forms.ModelForm):
    inscriptos = forms.IntegerField(required = True, min_value = 1)

    class Meta:
        model = CohorteEstablecimiento
        exclude = ('establecimiento', 'cohorte', 'estado',)

