# -*- coding: utf-8 -*-
from apps.registro.models.AnexoInformacionEdilicia import AnexoInformacionEdilicia
from apps.registro.models.Nivel import Nivel
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.TipoDominio import TipoDominio
from django.core.exceptions import ValidationError
from django import forms


class AnexoInformacionEdiliciaForm(forms.ModelForm):
    niveles = forms.ModelMultipleChoiceField(queryset=Nivel.objects.all().order_by('nombre'), widget=forms.CheckboxSelectMultiple, required=False)
    verificado = forms.BooleanField(required=False)

    class Meta:
        model = AnexoInformacionEdilicia
        exclude = ['anexo']

    def clean_tipo_compartido(self):
        tipo_compartido = None
        try:
            tipo_dominio = self.cleaned_data['tipo_dominio']
            tipo_compartido = self.cleaned_data['tipo_compartido']
            if tipo_dominio.id == TipoDominio.objects.get(descripcion='Compartido').id:
                if tipo_compartido is None:
                    raise ValidationError('Si el uso del edificio es compartido, debe detallar lo siguiente.')
        except KeyError:
            pass
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
