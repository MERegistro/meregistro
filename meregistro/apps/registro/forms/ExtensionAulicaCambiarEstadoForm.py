# -*- coding: utf-8 -*-
from django import forms
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica


class ExtensionAulicaCambiarEstadoForm(forms.Form):
    estado = forms.ModelChoiceField(queryset=EstadoExtensionAulica.objects, label='estado')
