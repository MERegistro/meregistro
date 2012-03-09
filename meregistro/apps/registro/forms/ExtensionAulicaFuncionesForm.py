# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Funcion import Funcion
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaFuncionesForm(ModelForm):
    funciones = forms.ModelMultipleChoiceField(queryset = Funcion.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)

    class Meta:
        model = Funcion
        fields = ['funciones']

    def clean_funciones(self):
        return self.cleaned_data['funciones']
