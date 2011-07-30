# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Titulo, TituloJurisdiccional, EstadoTitulo, EstadoTituloJurisdiccional, NormativaJurisdiccional, TituloOrientacion


class TituloJurisdiccionalForm(forms.ModelForm):
    orientaciones = forms.ModelMultipleChoiceField(queryset = TituloOrientacion.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    normativas = forms.ModelMultipleChoiceField(queryset = NormativaJurisdiccional.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)
    estado = forms.ModelChoiceField(queryset = EstadoTituloJurisdiccional.objects.all().order_by('nombre'), required = False, empty_label = None)

    class Meta:
        model = TituloJurisdiccional
        exclude = ('estado', 'jurisdiccion')

    " Sobreescribo el init "
    def __init__(self, *args, **kwargs):
        super(TituloJurisdiccionalForm, self).__init__(*args, **kwargs)
        self.fields['titulo'].queryset = Titulo.objects.filter(estado__nombre = EstadoTitulo.VIGENTE)
        self.fields['titulo'].empty_label = u'---Seleccione un tipo de título---'