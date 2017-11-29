# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from apps.registro.models import Establecimiento, AutoridadCargo, EstablecimientoAutoridad
from apps.seguridad.models import TipoDocumento
from django.core.exceptions import ValidationError
import dates

class EstablecimientoAutoridadForm(ModelForm):
    cargo = forms.ModelChoiceField(queryset=AutoridadCargo.objects.order_by('id'), label='Cargo', required=True, empty_label=None)
    tipo_documento = forms.ModelChoiceField(queryset=TipoDocumento.objects.order_by('descripcion'), label='Tipo de documento', required=False)
    fecha_nacimiento = forms.DateField(
        input_formats=['%d/%m/%Y', '%d/%m/%y'],
        required=False,
        widget=forms.DateInput(attrs={'class':'datePicker', 'readonly':'true'}))

    class Meta:
        model = EstablecimientoAutoridad


    def clean_fecha_nacimiento(self):
        try:
            f = self.cleaned_data['fecha_nacimiento']
            if f is not None and not dates.mayor_de_edad(f):
                raise ValidationError('Debe ser mayor de edad (21 años)')
        except KeyError:
            return None
        return f
