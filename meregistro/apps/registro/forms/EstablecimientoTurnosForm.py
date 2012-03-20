# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from apps.registro.models.Turno import Turno
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoTurnosForm(ModelForm):
    turnos = forms.ModelMultipleChoiceField(queryset = Turno.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = Turno
        fields = ['turnos']

    def clean_turnos(self):
        return self.cleaned_data['turnos']
