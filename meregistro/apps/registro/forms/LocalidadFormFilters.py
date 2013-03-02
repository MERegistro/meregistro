# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Localidad

class LocalidadFormFilters(forms.Form):
  def buildQuery(self, q=None):
    """
    Crea o refina un query de búsqueda.
    """
    if q is None:
      q = Localidad.objects.all()
    return q
