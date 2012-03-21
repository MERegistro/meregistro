# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from apps.registro.models import Establecimiento, AutoridadCargo, EstablecimientoAutoridad
from apps.seguridad.models import TipoDocumento
from django.core.exceptions import ValidationError


class EstablecimientoAutoridadForm(ModelForm):
    cargo = forms.ModelChoiceField(queryset=AutoridadCargo.objects.order_by('descripcion'), label='Cargo', required=True, empty_label=None)
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.order_by('descripcion'), label='Tipo de documento', required=False)
    fecha_nacimiento = forms.DateField(
        input_formats=['%d/%m/%Y', '%d/%m/%y'],
        required=False,
        widget=forms.TextInput(attrs={'class':'datePicker', 'readonly':'true'}))

    class Meta:
        model = EstablecimientoAutoridad
