# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Nivel import Nivel
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoNivelesForm(ModelForm):
    niveles = forms.ModelMultipleChoiceField(queryset = Nivel.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)

    class Meta:
        model = Nivel
        fields = ['niveles']

    def clean_niveles(self):
        return self.cleaned_data['niveles']
