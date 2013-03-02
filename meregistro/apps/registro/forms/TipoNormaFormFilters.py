# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import TipoNorma

class TipoNormaFormFilters(forms.Form):
  def buildQuery(self, q=None):
    """
    Crea o refina un query de búsqueda.
    """
    if q is None:
      q = TipoNorma.objects.all()
    return q
