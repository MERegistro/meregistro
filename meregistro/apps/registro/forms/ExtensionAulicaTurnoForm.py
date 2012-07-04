# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.Turno import Turno
from apps.registro.models.ExtensionAulicaTurno import ExtensionAulicaTurno
from apps.registro.models.Nivel import Nivel
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.TipoDominio import TipoDominio
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaTurnoForm(ModelForm):
    turno = forms.ModelChoiceField(queryset=Turno.objects.all(), required=True)
    niveles = forms.ModelMultipleChoiceField(queryset=Nivel.objects.all().order_by('nombre'), widget=forms.CheckboxSelectMultiple, required=False)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = ExtensionAulicaTurno
        exclude = ('extension_aulica', )

    def __init__(self, *args, **kwargs):
        self.extension_aulica_id = kwargs.pop('extension_aulica_id')
        super(ExtensionAulicaTurnoForm, self).__init__(*args, **kwargs)
        # no incluir los turnos ya existentes
        extension_aulica_tur = ExtensionAulicaTurno.objects.filter(extension_aulica__id=self.extension_aulica_id).exclude(turno__id=self.instance.turno_id)
        ids_actuales = [a.turno_id for a in extension_aulica_tur]
        self.fields['turno'].queryset = self.fields['turno'].queryset.exclude(id__in=ids_actuales)
        
    def clean_tipo_compartido(self):
        try:
            tipo_dominio = self.cleaned_data['tipo_dominio']
            tipo_compartido = self.cleaned_data['tipo_compartido']
            if tipo_dominio.id == TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id:
                if tipo_compartido is None:
                    raise ValidationError('Si el uso del edificio es compartido, debe detallar lo siguiente.')
        except KeyError:
            return None
        return tipo_compartido

    def clean_niveles(self):
        niveles = self.cleaned_data['niveles']
        try:
            tipo_compartido = self.cleaned_data['tipo_compartido']
            if tipo_compartido is not None and tipo_compartido.id == TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id:
                if len(niveles) == 0:
                    raise ValidationError('Debe especificar con qué niveles comparte el edificio.')
        except KeyError:
            pass
        return niveles
