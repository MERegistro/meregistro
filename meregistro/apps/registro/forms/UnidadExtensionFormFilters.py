# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import TipoDocumento, Usuario
from apps.registro.models import Establecimiento, UnidadExtension


class UnidadExtensionFormFilters(forms.Form):
    nombre = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    establecimiento = forms.ModelChoiceField(queryset = Establecimiento.objects.order_by('nombre'), label ='Establecimiento', required = False)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = UnidadExtension.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('nombre'):
            q = q.filter(nombre__icontains = self.cleaned_data['nombre'])
        if filter_by('establecimiento'):
            q = q.filter(establecimiento = self.cleaned_data['establecimiento'])
        return q
