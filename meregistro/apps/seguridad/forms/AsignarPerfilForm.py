# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import Ambito, Rol


class AsignarPerfilForm(forms.Form):
    rol = forms.ModelChoiceField(queryset=Rol.objects, label='rol', empty_label=None)
    ambito = forms.ModelChoiceField(queryset=Ambito.objects, label='ambito')

    def clean(self):
        if self.cleaned_data.has_key('rol') and self.cleaned_data.has_key('ambito') and not self.cleaned_data['rol'].asignableAAmbito(self.cleaned_data['ambito']):
            self._errors['rol'] = self.error_class([u'El rol no puede asignarse al ámbito seleccionado'])
        return self.cleaned_data
