# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import TipoDocumento, Usuario
from apps.registro.models import Establecimiento, Anexo, ExtensionAulica, DependenciaFuncional, Jurisdiccion, EstadoEstablecimiento, Localidad, Departamento, TipoGestion
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica


class UnidadesEducativasFormFilters(forms.Form):
    nombre = forms.CharField(max_length=40, label='Nombre', required=False)
    cue = forms.CharField(max_length=40, label='Cue', required=False)
    dependencia_funcional = forms.ModelChoiceField(queryset=DependenciaFuncional.objects, label='Dependencia funcional', required=False)
    jurisdiccion = forms.ModelChoiceField(queryset=Jurisdiccion.objects.order_by('nombre'), label='Jurisdiccion', required=False)
    departamento = forms.ModelChoiceField(queryset=Departamento.objects.order_by('nombre'), label='Departamento', required=False)
    localidad = forms.ModelChoiceField(queryset=Localidad.objects.order_by('nombre'), label='Localidad', required=False)
    estado = forms.ModelChoiceField(queryset=EstadoEstablecimiento.objects, label='Estado', required=False)
    tipo_gestion = forms.ModelChoiceField(queryset=TipoGestion.objects.order_by('nombre'), label='Tipo de gestión', required=False)
    estado = forms.ModelChoiceField(queryset=EstadoEstablecimiento.objects.order_by('nombre'), label='Estado', required=False)
    tipo_unidad_educativa = forms.ChoiceField(choices = (('', '---------'),('Establecimiento', 'Sede'), ('Anexo', 'Anexo'), ('ExtensionAulica', 'Extenión Áulica')), label='Tipo de Unidad Educativa', required=False)

    def __init__(self, *args, **kwargs):
        self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
        self.departamento_id = kwargs.pop('departamento_id')
        super(UnidadesEducativasFormFilters, self).__init__(*args, **kwargs)
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
            q1 = Establecimiento.objects.all().order_by('nombre').extra(select={'tipo_ue': '\'Sede\''})
            q2 = Anexo.objects.all().order_by('nombre').extra(select={'tipo_ue': '\'Anexo\''})
            q3 = ExtensionAulica.objects.all().order_by('nombre').extra(select={'tipo_ue': '\'Extensión Áulica\''})
        if self.is_valid():
            def filter_by(field):
                return self.cleaned_data.has_key(field) and self.cleaned_data[field] != '' and self.cleaned_data[field] is not None
            if filter_by('nombre'):
                q1 = q1.filter(nombre__icontains=self.cleaned_data['nombre'])
                q2 = q2.filter(nombre__icontains=self.cleaned_data['nombre'])
                q3 = q3.filter(nombre__icontains=self.cleaned_data['nombre'])
            if filter_by('cue'):
                q1 = q1.filter(cue__exact=self.cleaned_data['cue'])
                q2 = q2.filter(cue__exact=self.cleaned_data['cue'])
                q3 = q3.filter(cue__exact=self.cleaned_data['cue'])
            if filter_by('dependencia_funcional'):
                q1 = q1.filter(dependencia_funcional=self.cleaned_data['dependencia_funcional'])
                q2 = q2.filter(dependencia_funcional=self.cleaned_data['dependencia_funcional'])
                q3 = q3.filter(dependencia_funcional=self.cleaned_data['dependencia_funcional'])
            if filter_by('jurisdiccion'):
                q1 = q1.filter(dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
                q2 = q2.filter(dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
                q3 = q3.filter(dependencia_funcional__jurisdiccion=self.cleaned_data['jurisdiccion'])
            if filter_by('estado'):
                q1 = q1.filter(estado=self.cleaned_data['estado'])
                q2 = q2.filter(estado=self.cleaned_data['estado'])
                q3 = q3.filter(estado=self.cleaned_data['estado'])
            if filter_by('departamento'):
                q1 = q1.filter(domicilios__localidad__departamento=self.cleaned_data['departamento'])
                q2 = q2.filter(domicilios__localidad__departamento=self.cleaned_data['departamento'])
                q3 = q3.filter(domicilios__localidad__departamento=self.cleaned_data['departamento'])
            if filter_by('localidad'):
                q1 = q1.filter(domicilios__localidad=self.cleaned_data['localidad'])
                q2 = q2.filter(domicilios__localidad=self.cleaned_data['localidad'])
                q3 = q3.filter(domicilios__localidad=self.cleaned_data['localidad'])
            if filter_by('tipo_gestion'):
                q1 = q1.filter(dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])
                q2 = q2.filter(dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])
                q3 = q3.filter(dependencia_funcional__tipo_gestion=self.cleaned_data['tipo_gestion'])
            if filter_by('estado'):
                q1 = q1.filter(estado=self.cleaned_data['estado'])
                q2 = q2.filter(estado=self.cleaned_data['estado'])
                q3 = q3.filter(estado=self.cleaned_data['estado'])
            if filter_by('tipo_unidad_educativa'):
                tipo_ue = self.cleaned_data['tipo_unidad_educativa']
                if tipo_ue == 'Establecimiento':
                    resultado = {'sedes': q1.distinct(), 'anexos': q2.none(), 'extensiones_aulicas': q3.none()}
                elif tipo_ue == 'Anexo':
                    resultado = {'sedes': q1.none(), 'anexos': q2.distinct(), 'extensiones_aulicas': q3.none()}
                elif tipo_ue == 'ExtensionAulica':
                    resultado = {'sedes': q1.none(), 'anexos': q2.none(), 'extensiones_aulicas': q3.distinct()}
            else:
                resultado = {'sedes': q1.distinct(), 'anexos': q2.distinct(), 'extensiones_aulicas': q3.distinct()}
        return resultado
