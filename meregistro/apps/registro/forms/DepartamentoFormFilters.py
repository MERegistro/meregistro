# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Departamento

class DepartamentoFormFilters(forms.Form):
  def buildQuery(self, q=None):
    """
    Crea o refina un query de búsqueda.
    """
    if q is None:
      q = Departamento.objects.all()
    return q
