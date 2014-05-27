# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import NormativaJurisdiccional, EstadoNormativaJurisdiccional, TipoNormativaJurisdiccional, NormativaMotivoOtorgamiento


class NormativaPostituloJurisdiccionalForm(forms.ModelForm):
    tipo_normativa_jurisdiccional = forms.ModelChoiceField(queryset = TipoNormativaJurisdiccional.objects.order_by('nombre'), label = 'Tipo de normativa')
    otorgada_por = forms.ModelChoiceField(queryset = NormativaMotivoOtorgamiento.objects.order_by('nombre'), label = 'Otorgada por')
    estado = forms.ModelChoiceField(queryset = EstadoNormativaJurisdiccional.objects.all().order_by('nombre'))
    observaciones = forms.CharField(widget = forms.Textarea, required = False)

    class Meta:
        model = NormativaJurisdiccional
        exclude = ('jurisdiccion')
