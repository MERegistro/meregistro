# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Titulo, Area, Carrera, EstadoTitulo
from apps.registro.models import Nivel, Jurisdiccion


class TituloForm(forms.ModelForm):
    carrera = forms.ModelChoiceField(queryset = Carrera.objects.order_by('nombre'), label = 'Carrera')
    areas = forms.ModelMultipleChoiceField(queryset = Area.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple)
    niveles = forms.ModelMultipleChoiceField(queryset = Nivel.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple)
    jurisdicciones = forms.ModelMultipleChoiceField(queryset = Jurisdiccion.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple)
    observaciones = forms.CharField(widget = forms.Textarea, required = False)
    estado = forms.ModelChoiceField(queryset = EstadoTitulo.objects.all().order_by('nombre'), required = False, empty_label = None)

    class Meta:
        model = Titulo
        exclude = ('estado')
