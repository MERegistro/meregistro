# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import Ambito, Rol


class AsignarPerfilForm(forms.Form):
    rol = forms.ModelChoiceField(queryset=Rol.objects, label='rol', empty_label=None)
    ambito = forms.ModelChoiceField(queryset=Ambito.objects, label='ambito')
