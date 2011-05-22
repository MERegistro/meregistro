# -*- coding: utf-8 -*-
from django import forms
from meregistro.registro.models.Estado import Estado


class EstablecimientoCambiarEstadoForm(forms.Form):
    estado = forms.ModelChoiceField(queryset=Estado.objects, label='estado')
    observaciones = forms.CharField(required=False, widget=forms.Textarea)
