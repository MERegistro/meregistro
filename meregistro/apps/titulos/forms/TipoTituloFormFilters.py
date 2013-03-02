# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import TipoTitulo

class TipoTituloFormFilters(forms.Form):
  def buildQuery(self, q=None):
    """
    Crea o refina un query de búsqueda.
    """
    if q is None:
      q = TipoTitulo.objects.all()
    return q
