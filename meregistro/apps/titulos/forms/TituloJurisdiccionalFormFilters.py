# -*- coding: UTF-8 -*-

from django import forms
from apps.titulos.models import TituloJurisdiccional, Carrera, EstadoTituloJurisdiccional, TipoTitulo


class TituloJurisdiccionalFormFilters(forms.Form):

    nombre = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    tipo_titulo = forms.ModelChoiceField(queryset = TipoTitulo.objects.order_by('nombre'), label = 'Tipo de título', required = False)
    carrera = forms.ModelChoiceField(queryset = Carrera.objects.all().order_by('nombre'), required = False)
    estado = forms.ModelChoiceField(queryset = EstadoTituloJurisdiccional.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = TituloJurisdiccional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('nombre'):
            q = q.filter(nombre__icontains = self.cleaned_data['nombre'])
        if filter_by('tipo_titulo'):
            q = q.filter(tipo_titulo = self.cleaned_data['tipo_titulo'])
        if filter_by('estado'):
            q = q.filter(estado = self.cleaned_data['estado'])
        if filter_by('carrera'):
            q = q.filter(titulo__carrera = self.cleaned_data['carrera'])
        return q
