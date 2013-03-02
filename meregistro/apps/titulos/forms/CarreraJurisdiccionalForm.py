# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Carrera, CarreraJurisdiccional, EstadoCarrera, EstadoCarreraJurisdiccional, NormativaJurisdiccional, TituloOrientacion


class CarreraJurisdiccionalForm(forms.ModelForm):
    #orientaciones = forms.ModelMultipleChoiceField(queryset = TituloOrientacion.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    normativas = forms.ModelMultipleChoiceField(queryset = NormativaJurisdiccional.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    estado = forms.ModelChoiceField(queryset = EstadoCarreraJurisdiccional.objects.all().order_by('nombre'), required = False, empty_label = None)

    class Meta:
        model = CarreraJurisdiccional
        exclude = ('estado', 'jurisdiccion')

    " Sobreescribo el init "
    def __init__(self, *args, **kwargs):
        super(CarreraJurisdiccionalForm, self).__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.filter(estado__nombre = EstadoCarrera.VIGENTE)
        self.fields['carrera'].empty_label = u'---Seleccione un tipo de título---'
