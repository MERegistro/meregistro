# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import EgresadosEstablecimiento, EgresadosEstablecimientoDetalle



class EgresadosEstablecimientoDetalleForm(forms.ModelForm):

    ANIOS_CHOICES = [('', '-------')] + [(i, i) for i in range(1980, 2021)]

    anio_ingreso = forms.ChoiceField(label = 'Año', choices = ANIOS_CHOICES, required = True)
    cantidad_egresados = forms.IntegerField(required = True, min_value = 1)
    

    class Meta:
        model = EgresadosEstablecimientoDetalle
        exclude = ('egresados_establecimiento',)
        
    "Le agrego datos para chequear"
    def __init__(self, *args, **kwargs):
        self.egresados_establecimiento_id = kwargs.pop('egresados_establecimiento_id')
        super(EgresadosEstablecimientoDetalleForm, self).__init__(*args, **kwargs)

    def clean_anio_ingreso(self):
        egresados = EgresadosEstablecimiento.objects.get(pk = self.egresados_establecimiento_id)
        if int(self.cleaned_data['anio_ingreso']) >= egresados.anio:
            raise ValidationError("El año de ingreso debe ser menor que el año de egreso.")
            
        try:
            registro = EgresadosEstablecimientoDetalle.objects.get(anio_ingreso = self.cleaned_data['anio_ingreso'], egresados_establecimiento = self.egresados_establecimiento_id)
        except:
            registro = None
        if registro is not None and registro.id != self.instance.id:
            raise ValidationError("Ya se detalló ese año para el año de egresados")
        return self.cleaned_data['anio_ingreso']
