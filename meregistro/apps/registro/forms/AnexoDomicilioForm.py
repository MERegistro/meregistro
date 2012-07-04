# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.Anexo import Anexo
from apps.registro.models.AnexoDomicilio import AnexoDomicilio
from apps.registro.models.TipoDomicilio import TipoDomicilio
from apps.registro.models.Departamento import Departamento
from django.core.exceptions import ValidationError
from django import forms


class AnexoDomicilioForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(queryset = Departamento.objects.order_by('nombre'), label = 'Departamento', required = False)

    class Meta:
        model = AnexoDomicilio
        exclude = ('anexo')

    def __init__(self, *args, **kwargs):
        self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
        self.anexo_id = kwargs.pop('anexo_id')
        super(AnexoDomicilioForm, self).__init__(*args, **kwargs)
        "Para no cargar todas las localidades y departamentos"
        self.fields['departamento'].queryset = self.fields['departamento'].queryset.filter(jurisdiccion__id=self.jurisdiccion_id)
        self.fields['localidad'].queryset = self.fields['localidad'].queryset.filter(departamento__jurisdiccion__id=self.jurisdiccion_id)

    def clean_tipo_domicilio(self):
        tipo_domicilio = self.cleaned_data['tipo_domicilio']
        try:
            dom_existente = AnexoDomicilio.objects.get(tipo_domicilio__id=tipo_domicilio.id, anexo__id=self.anexo_id)
        except AnexoDomicilio.DoesNotExist:
            dom_existente = None
        " Si ya hay un domicilio para este anexo "
        if dom_existente and dom_existente != self.instance:
            msg = "Ya hay un domicilio %s cargado." % (str(tipo_domicilio.descripcion).lower())
            raise ValidationError(msg)
        return tipo_domicilio

