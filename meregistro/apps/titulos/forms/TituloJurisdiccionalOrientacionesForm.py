# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccional, TituloOrientacion


class TituloJurisdiccionalOrientacionesForm(forms.ModelForm):
    orientaciones = forms.ModelMultipleChoiceField(queryset = TituloOrientacion.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)

    class Meta:
       model = TituloJurisdiccional
       fields = ('orientaciones',)

