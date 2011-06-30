# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import MotivoBloqueo


class BloquearUsuarioForm(forms.Form):
    motivo = forms.ModelChoiceField(queryset=MotivoBloqueo.objects.filter(accion='L'), required=True)
