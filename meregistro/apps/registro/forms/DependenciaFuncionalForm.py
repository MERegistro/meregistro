# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.core.exceptions import ValidationError
from apps.registro.models import DependenciaFuncional, Jurisdiccion, TipoGestion


class DependenciaFuncionalForm(ModelForm):
    nombre = forms.CharField(max_length=255, required=False)
    jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.all().order_by('nombre'), required=True, empty_label=None)
    tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.all().order_by('nombre'), required=True, empty_label=None)

    class Meta:
        model = DependenciaFuncional

    def clean(self):
        cleaned_data = self.cleaned_data
        "Arma el nombre con los valores enviados"
        jurisdiccion = cleaned_data['jurisdiccion']
        tipo_gestion = cleaned_data['tipo_gestion']
        try:
            tipo_dependencia_funcional = cleaned_data['tipo_dependencia_funcional'].nombre
        except KeyError:
            tipo_dependencia_funcional = u""
        cleaned_data['nombre'] = tipo_dependencia_funcional + u" de Gestión " + tipo_gestion.nombre + u" de " + jurisdiccion.nombre
        return cleaned_data
