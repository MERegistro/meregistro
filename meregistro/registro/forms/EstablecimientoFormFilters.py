# -*- coding: UTF-8 -*-

from django import forms
from seguridad.models import TipoDocumento, Usuario
from registro.models import Establecimiento, DependenciaFuncional, Jurisdiccion, Estado


class EstablecimientoFormFilters(forms.Form):
    nombre = forms.CharField(max_length=40, label='Nombre', required=False)
    cue = forms.CharField(max_length=40, label='Cue', required=False)
    dependencia_funcional = forms.ModelChoiceField(queryset=DependenciaFuncional.objects, label='Dependencia funcional', required=False)
    estado = forms.ModelChoiceField(queryset=Estado.objects, label='Estado', required=False)
    jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects, label='Jurisdiccion', required=False)

    def buildQuery(self, q=None):
        """
        Crea o refina un query de búsqueda.
        """
        if q is None:
            q = Establecimiento.objects.all()
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
        if filter_by('nombre'):
            q = q.filter(nombre__icontains=self.cleaned_data['nombre'])
        if filter_by('cue'):
            q = q.filter(cue__contains=self.cleaned_data['cue'])
        if filter_by('dependencia_funcional'):
            q = q.filter(dependencia_funcional=self.cleaned_data['dependencia_funcional'])
        if filter_by('jurisdiccion'):
            q = q.filter(dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
        return q
