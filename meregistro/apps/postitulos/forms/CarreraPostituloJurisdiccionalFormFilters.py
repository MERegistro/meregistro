# -*- coding: UTF-8 -*-

from django import forms
from apps.postitulos.models import CarreraPostituloJurisdiccional, CarreraPostitulo, EstadoCarreraPostituloJurisdiccional, TipoPostitulo
import datetime

class CarreraPostituloJurisdiccionalFormFilters(forms.Form):

    carrera_postitulo = forms.CharField(required = False)
    estado = forms.ModelChoiceField(queryset = EstadoCarreraPostituloJurisdiccional.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = CarreraPostituloJurisdiccional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        if filter_by('carrera'):
            q = q.filter(carrera_postitulo__nombre__icontains = self.cleaned_data['carrera_postitulo'])
        return q
