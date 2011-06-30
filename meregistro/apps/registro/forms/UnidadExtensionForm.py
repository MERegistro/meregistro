# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.UnidadExtension import UnidadExtension
from apps.registro.models.Turno import Turno
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


currentYear = datetime.datetime.now().year


class UnidadExtensionForm(forms.ModelForm):
    observaciones = forms.CharField(required = False, widget = forms.Textarea)
    fecha_alta = forms.DateField(input_formats = ['%d/%m/%Y', '%d/%m/%y'], required = False, initial = datetime.date.today)
    turnos = forms.ModelMultipleChoiceField(queryset = Turno.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)

    class Meta:
        model = UnidadExtension
        exclude = ['establecimiento']
