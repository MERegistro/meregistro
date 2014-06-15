# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.postitulos.models import NormativaPostituloJurisdiccional, EstadoNormativaPostituloJurisdiccional, TipoNormativaPostituloJurisdiccional, NormativaMotivoOtorgamiento


class NormativaPostituloJurisdiccionalForm(forms.ModelForm):
    tipo_normativa_postitulo_jurisdiccional = forms.ModelChoiceField(queryset = TipoNormativaPostituloJurisdiccional.objects.order_by('nombre'), label = 'Tipo de normativa')
    otorgada_por = forms.ModelChoiceField(queryset = NormativaMotivoOtorgamiento.objects.order_by('nombre'), label = 'Otorgada por')
    estado = forms.ModelChoiceField(queryset = EstadoNormativaPostituloJurisdiccional.objects.all().order_by('nombre'))
    observaciones = forms.CharField(widget = forms.Textarea, required = False)

    class Meta:
        model = NormativaPostituloJurisdiccional
        exclude = ('jurisdiccion')
