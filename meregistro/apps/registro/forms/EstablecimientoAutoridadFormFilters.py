# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import EstablecimientoAutoridad


class EstablecimientoAutoridadFormFilters(forms.Form):
    establecimiento_id = None
    
    def __init__(self, *args, **kwargs):
        try:
            self.establecimiento_id = kwargs.pop('establecimiento_id')
        except KeyError:
            pass
        super(EstablecimientoAutoridadFormFilters, self).__init__(*args, **kwargs)
            
    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = EstablecimientoAutoridad.objects.all()
            if self.establecimiento_id is not None:
                q = q.filter(establecimiento__id = self.establecimiento_id)
        return q.order_by('apellido', 'nombre')
