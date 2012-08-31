# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import TipoDocumento, Usuario
from apps.registro.models import Establecimiento, DependenciaFuncional, Jurisdiccion, EstadoEstablecimiento, Localidad, Departamento, TipoGestion
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento


class EstablecimientoFormFilters(forms.Form):
    nombre = forms.CharField(max_length=40, label='Nombre', required=False)
    cue = forms.CharField(max_length=40, label='Cue', required=False)
    dependencia_funcional = forms.ModelChoiceField(queryset=DependenciaFuncional.objects, label='Dependencia funcional', required=False)
    jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdiccion', required=False)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.order_by('nombre'), label='Departamento', required=False)
    localidad = forms.ModelChoiceField(queryset=Localidad.objects.order_by('nombre'), label='Localidad', required=False)
    estado = forms.ModelChoiceField(queryset=EstadoEstablecimiento.objects, label='Estado', required=False)
    tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.order_by('nombre'), label='Tipo de gestión', required=False)
    estado = forms.ModelChoiceField(queryset=EstadoEstablecimiento.objects.order_by('nombre'), label='Estado', required=False)

    def __init__(self, *args, **kwargs):
        self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
        self.departamento_id = kwargs.pop('departamento_id')
        super(EstablecimientoFormFilters, self).__init__(*args, **kwargs)
        "Para no cargar todas las localidades y departamentos"
        if self.jurisdiccion_id is not None:
            self.fields['departamento'].queryset = self.fields['departamento'].queryset.filter(jurisdiccion__id=self.jurisdiccion_id)
        if self.departamento_id is not None:
            self.fields['localidad'].queryset = self.fields['localidad'].queryset.filter(departamento__id=self.departamento_id)
        else:
            self.fields['localidad'].queryset = self.fields['localidad'].queryset.none()
        self.fields['dependencia_funcional'].widget.attrs['style'] = 'width: 600px'

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
                q = q.filter(cue__exact=self.cleaned_data['cue'])
            if filter_by('dependencia_funcional'):
                q = q.filter(dependencia_funcional=self.cleaned_data['dependencia_funcional'])
            if filter_by('jurisdiccion'):
                q = q.filter(dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
            if filter_by('estado'):
                q = q.filter(estado=self.cleaned_data['estado'])
            if filter_by('departamento'):
                q = q.filter(domicilios__localidad__departamento=self.cleaned_data['departamento'])
            if filter_by('localidad'):
                q = q.filter(domicilios__localidad=self.cleaned_data['localidad'])
            if filter_by('tipo_gestion'):
                q = q.filter(dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])
            if filter_by('estado'):
                q = q.filter(estado=self.cleaned_data['estado'])
        return q.distinct()
