# -*- coding: UTF-8 -*-

from django import forms
from apps.registro.models import Establecimiento, DependenciaFuncional, Localidad, EstadoEstablecimiento


class CohorteAsignarEstablecimientosFormFilters(forms.Form):
    nombre = forms.CharField(max_length=40, label='Nombre', required=False)
    cue = forms.CharField(max_length=40, label='Cue', required=False)
    dependencia_funcional = forms.ModelChoiceField(queryset=DependenciaFuncional.objects, label='Dependencia funcional', required=False)
    localidad = forms.ModelChoiceField(queryset=Localidad.objects, label='Localidad', required=False)

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
            if filter_by('localidad'):
                q = q.filter(domicilios__localidad=self.cleaned_data['localidad'])

        return q.filter(estado__nombre=EstadoEstablecimiento.REGISTRADO)
