# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import Rol


class RolFormFilters(forms.Form):
    descripcion = forms.CharField(max_length=50, label='descripcion', required=False)
    nombre = forms.CharField(max_length=50, label='nombre', required=False)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = Rol.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
            if filter_by('nombre'):
                q = q.filter(nombre__istartswith=self.cleaned_data['nombre'])
            if filter_by('descripcion'):
                q = q.filter(descripcion__istartswith=self.cleaned_data['descripcion'])
        return q
