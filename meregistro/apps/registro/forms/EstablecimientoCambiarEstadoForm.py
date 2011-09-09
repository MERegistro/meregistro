# -*- coding: utf-8 -*-
from django import forms
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento


class EstablecimientoCambiarEstadoForm(forms.Form):
    estado = forms.ModelChoiceField(queryset = EstadoEstablecimiento.objects, label = 'estado')
    observaciones = forms.CharField(required = False, widget = forms.Textarea)
