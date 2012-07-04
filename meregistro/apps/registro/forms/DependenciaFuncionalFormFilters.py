# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import DependenciaFuncional, Jurisdiccion, TipoGestion, TipoDependenciaFuncional, TipoEducacion


class DependenciaFuncionalFormFilters(forms.Form):
    jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdicción', required=False)
    tipo_dependencia_funcional = forms.ModelChoiceField(queryset=TipoDependenciaFuncional.objects.order_by('nombre'), label='Tipo de dependencia', required=False)
    tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.order_by('nombre'), label='Tipo de gestión', required=False)
    nombre = forms.CharField(max_length=50, label='Nombre', required=False)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = DependenciaFuncional.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('nombre'):
            q = q.filter(nombre__icontains=self.cleaned_data['nombre'])
        if filter_by('jurisdiccion'):
            q = q.filter(jurisdiccion=self.cleaned_data['jurisdiccion'])
        if filter_by('tipo_gestion'):
            q = q.filter(tipo_gestion=self.cleaned_data['tipo_gestion'])
        if filter_by('tipo_dependencia_funcional'):
            q = q.filter(tipo_dependencia_funcional=self.cleaned_data['tipo_dependencia_funcional'])
        return q
