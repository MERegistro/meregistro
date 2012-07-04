# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Alcance import Alcance
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoAlcancesForm(ModelForm):
    alcances = forms.ModelMultipleChoiceField(queryset=Alcance.objects.all().order_by('nombre'), widget=forms.CheckboxSelectMultiple, required=False)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = Alcance
        fields = ['alcances']

    def clean_alcances(self):
        return self.cleaned_data['alcances']
