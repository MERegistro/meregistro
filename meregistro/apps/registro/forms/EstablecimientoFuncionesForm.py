# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Establecimiento
from apps.registro.models.Funcion import Funcion
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoFuncionesForm(ModelForm):
    funciones = forms.ModelMultipleChoiceField(queryset = Funcion.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = Funcion
        fields = ['funciones']

    def clean_funciones(self):
        return self.cleaned_data['funciones']
