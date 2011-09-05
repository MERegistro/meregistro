# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Matricula
from apps.registro.models import Establecimiento


class MatriculaForm(forms.ModelForm):
    observaciones = forms.CharField(widget = forms.Textarea, required = False)
    establecimiento = forms.ModelChoiceField(queryset = Establecimiento.objects.order_by('nombre'), required = True, empty_label = None)
    class Meta:
        model = Matricula
