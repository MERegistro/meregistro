# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccional, NormativaJurisdiccional


class TituloJurisdiccionalNormativasForm(forms.ModelForm):
    normativas = forms.ModelMultipleChoiceField(queryset = NormativaJurisdiccional.objects.all().order_by('numero_anio'), widget = forms.CheckboxSelectMultiple, required = False)

    class Meta:
       model = TituloJurisdiccional
       fields = ('normativas',)

