# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Carrera, CarreraJurisdiccional, EstadoCarrera
from apps.titulos.forms import CarreraJurisdiccionalForm


class CarreraJurisdiccionalDatosBasicosForm(forms.ModelForm):
    carrera = forms.ModelChoiceField(queryset = Carrera.objects.order_by('nombre'), label = 'Nombre', required = True)
    
    class Meta:
       model = CarreraJurisdiccional
       fields = ('carrera',)

    def __init__(self, *args, **kwargs):
        self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
        super(CarreraJurisdiccionalDatosBasicosForm, self).__init__(*args, **kwargs)
        "Para no cargar quichicientosmil"
        self.fields['carrera'].queryset = self.fields['carrera'].queryset.filter(jurisdicciones__id = self.jurisdiccion_id, estado__nombre = EstadoCarrera.VIGENTE)
