# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import Titulo, EstadoTituloOrientacion, TituloOrientacion


class TituloOrientacionFormFilters(forms.Form):
    nombre = forms.CharField(max_length = 40, label = 'Nombre', required = False)
    titulo = forms.ModelChoiceField(queryset = Titulo.objects.all().order_by('nombre'), required = False)

    def buildQuery(self, q = None):
        "Crea o refina un query de búsqueda."
        if q is None:
            q = TituloOrientacion.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('nombre'):
            q = q.filter(nombre__icontains=self.cleaned_data['nombre'])
        if filter_by('titulo'):
            q = q.filter(titulo__id = self.cleaned_data['titulo'].id)
        return q
