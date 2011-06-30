# -*- coding: utf-8 -*-
from django import forms
import datetime
from meregistro.apps.registro.models.AnexoBaja import AnexoBaja


class AnexoBajaForm(forms.ModelForm):
    observaciones = forms.CharField(required=False, widget=forms.Textarea)
    fecha_baja = forms.DateField(input_formats = ['%d/%m/%Y', '%d/%m/%y'], required = True, initial = datetime.date.today)

    class Meta:
        model = AnexoBaja
        exclude = ['anexo']
