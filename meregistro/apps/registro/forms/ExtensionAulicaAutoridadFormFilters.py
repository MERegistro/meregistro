# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import ExtensionAulicaAutoridad


class ExtensionAulicaAutoridadFormFilters(forms.Form):
    extension_aulica_id = None

    def __init__(self, *args, **kwargs):
        try:
            self.extension_aulica_id = kwargs.pop('extension_aulica_id')
        except KeyError:
            pass
        super(ExtensionAulicaAutoridadFormFilters, self).__init__(*args, **kwargs)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = ExtensionAulicaAutoridad.objects.all()
            if self.extension_aulica_id is not None:
                q = q.filter(extension_aulica__id=self.extension_aulica_id)
        return q.order_by('apellido', 'nombre')
