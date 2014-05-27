# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import CarreraPostitulo, CarreraPostituloJurisdiccional, EstadoCarreraPostitulo, EstadoCarreraPostituloJurisdiccional, NormativaPostitulo #, TituloOrientacion


class CarreraPostituloJurisdiccionalForm(forms.ModelForm):
    normativas = forms.ModelMultipleChoiceField(queryset = NormativaPostitulo.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    estado = forms.ModelChoiceField(queryset = EstadoCarreraPostituloJurisdiccional.objects.all().order_by('nombre'), required = False, empty_label = None)

    class Meta:
        model = CarreraPostituloJurisdiccional
        exclude = ('estado', 'jurisdiccion')

    " Sobreescribo el init "
    def __init__(self, *args, **kwargs):
        super(CarreraPostituloJurisdiccionalForm, self).__init__(*args, **kwargs)
        self.fields['carrera_postitulo'].queryset = CarreraPostitulo.objects.filter(estado__nombre = EstadoCarreraPostitulo.VIGENTE)
        self.fields['carrera_postitulo'].empty_label = u'---Seleccione un tipo de postítulo---'
