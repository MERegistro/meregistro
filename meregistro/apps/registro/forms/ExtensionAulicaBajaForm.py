# -*- coding: utf-8 -*-
from django import forms
import datetime
from apps.registro.models.ExtensionAulicaBaja import ExtensionAulicaBaja


class ExtensionAulicaBajaForm(forms.ModelForm):
    observaciones = forms.CharField(required=False, widget=forms.Textarea)
    fecha_baja = forms.DateField(input_formats = ['%d/%m/%Y', '%d/%m/%y'], required = True, initial = datetime.date.today)

    class Meta:
        model = ExtensionAulicaBaja
        exclude = ['extension_aulica']
