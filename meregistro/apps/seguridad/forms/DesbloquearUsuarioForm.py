# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import MotivoBloqueo


class DesbloquearUsuarioForm(forms.Form):
    motivo = forms.ModelChoiceField(queryset=MotivoBloqueo.objects.filter(accion='U'), required=True)
