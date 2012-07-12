# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Jurisdiccion

class JurisdiccionFormFilters(forms.Form):
  def buildQuery(self, q=None):
    """
    Crea o refina un query de búsqueda.
    """
    if q is None:
      q = Jurisdiccion.objects.all()
    return q
