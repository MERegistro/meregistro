# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import AnexoAutoridad


class AnexoAutoridadFormFilters(forms.Form):
    anexo_id = None

    def __init__(self, *args, **kwargs):
        try:
            self.anexo_id = kwargs.pop('anexo_id')
        except KeyError:
            pass
        super(AnexoAutoridadFormFilters, self).__init__(*args, **kwargs)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = AnexoAutoridad.objects.all()
            if self.anexo_id is not None:
                q = q.filter(anexo__id=self.anexo_id)
        return q.order_by('apellido', 'nombre')
