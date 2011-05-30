# -*- coding: utf-8 -*-
from meregistro.registro.models.EstablecimientoInformacionEdilicia import EstablecimientoInformacionEdilicia
from meregistro.registro.models.Nivel import Nivel
from meregistro.registro.models.TipoCompartido import TipoCompartido
from meregistro.registro.models.TipoDominio import TipoDominio
from django.core.exceptions import ValidationError
from django import forms


class EstablecimientoInformacionEdiliciaForm(forms.ModelForm):
    niveles = forms.ModelMultipleChoiceField(queryset = Nivel.objects.all().order_by('nombre'), widget = forms.CheckboxSelectMultiple, required = False)

    class Meta:
        model = EstablecimientoInformacionEdilicia
        exclude = ['establecimiento']

    def clean_tipo_compartido(self):
        try:
            tipo_dominio = self.cleaned_data['tipo_dominio']
            tipo_compartido = self.cleaned_data['tipo_compartido']
            if tipo_dominio.id == TipoDominio.objects.get(descripcion = 'Compartido').id:
                if tipo_compartido is None:
                    raise ValidationError('Si el uso del edificio es compartido, debe detallar lo siguiente.')
        except KeyError:
            pass
        return tipo_compartido

    def clean_niveles(self):
        niveles = self.cleaned_data['niveles']
        try:
            tipo_compartido = self.cleaned_data['tipo_compartido']
            if tipo_compartido.id == TipoCompartido.objects.get(descripcion = 'Establecimiento de otro nivel').id:
                if len(niveles) == 0:
                    raise ValidationError('Debe especificar con qué niveles comparte el edificio.')
        except KeyError:
            pass
        return niveles
