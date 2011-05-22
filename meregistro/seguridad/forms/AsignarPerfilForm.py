# -*- coding: UTF-8 -*-

from django import forms
from seguridad.models import Ambito, Rol


class AsignarPerfilForm(forms.Form):
    rol = forms.ModelChoiceField(queryset=Rol.objects, label='rol')
    ambito = forms.ModelChoiceField(queryset=Ambito.objects, label='ambito')
