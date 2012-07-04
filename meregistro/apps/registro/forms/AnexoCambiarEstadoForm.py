# -*- coding: utf-8 -*-
from django import forms
from apps.registro.models.EstadoAnexo import EstadoAnexo


class AnexoCambiarEstadoForm(forms.Form):
    estado = forms.ModelChoiceField(queryset=EstadoAnexo.objects, label='estado')
