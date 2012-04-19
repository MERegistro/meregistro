# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models import Anexo
from apps.registro.models.Turno import Turno
from apps.registro.models.AnexoTurno import AnexoTurno
from apps.registro.models.Nivel import Nivel
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.TipoDominio import TipoDominio
from django.core.exceptions import ValidationError
from django import forms


class AnexoTurnoForm(ModelForm):
    turno = forms.ModelChoiceField(queryset=Turno.objects.all(), required=True)
    niveles = forms.ModelMultipleChoiceField(queryset=Nivel.objects.all().order_by('nombre'), widget=forms.CheckboxSelectMultiple, required=False)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = AnexoTurno
        exclude = ('anexo', )

    def __init__(self, *args, **kwargs):
        self.anexo_id = kwargs.pop('anexo_id')
        super(AnexoTurnoForm, self).__init__(*args, **kwargs)
        # no incluir los turnos ya existentes
        anexo_tur = AnexoTurno.objects.filter(anexo__id=self.anexo_id).exclude(turno__id=self.instance.turno_id)
        ids_actuales = [a.turno_id for a in anexo_tur]
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
