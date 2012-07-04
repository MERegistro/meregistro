# -*- coding: utf-8 -*-
from django.forms import ModelForm
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.ExtensionAulicaDomicilio import ExtensionAulicaDomicilio
from apps.registro.models.TipoDomicilio import TipoDomicilio
from apps.registro.models.Departamento import Departamento
from django.core.exceptions import ValidationError
from django import forms


class ExtensionAulicaDomicilioForm(forms.ModelForm):
    departamento = forms.ModelChoiceField(queryset = Departamento.objects.order_by('nombre'), label = 'Departamento', required = False)

    class Meta:
        model = ExtensionAulicaDomicilio
        exclude = ('extension_aulica')

    def __init__(self, *args, **kwargs):
        self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
        self.extension_aulica_id = kwargs.pop('extension_aulica_id')
        super(ExtensionAulicaDomicilioForm, self).__init__(*args, **kwargs)
        "Para no cargar todas las localidades y departamentos"
        self.fields['departamento'].queryset = self.fields['departamento'].queryset.filter(jurisdiccion__id=self.jurisdiccion_id)
        self.fields['localidad'].queryset = self.fields['localidad'].queryset.filter(departamento__jurisdiccion__id=self.jurisdiccion_id)

    def clean_tipo_domicilio(self):
        tipo_domicilio = self.cleaned_data['tipo_domicilio']
        try:
            dom_existente = ExtensionAulicaDomicilio.objects.get(tipo_domicilio__id=tipo_domicilio.id, extension_aulica__id=self.extension_aulica_id)
        except ExtensionAulicaDomicilio.DoesNotExist:
            dom_existente = None
        " Si ya hay un domicilio para este extension_aulica "
        if dom_existente and dom_existente != self.instance:
            msg = "Ya hay un domicilio %s cargado." % (str(tipo_domicilio.descripcion).lower())
            raise ValidationError(msg)
        return tipo_domicilio

