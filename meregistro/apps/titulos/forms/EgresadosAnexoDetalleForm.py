# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import EgresadosAnexo, EgresadosAnexoDetalle



class EgresadosAnexoDetalleForm(forms.ModelForm):

    ANIOS_CHOICES = [('', '-------')] + [(i, i) for i in range(1980, 2021)]

    anio_ingreso = forms.ChoiceField(label = 'Año', choices = ANIOS_CHOICES, required = True)
    cantidad_egresados = forms.IntegerField(required = True, min_value = 1)
    

    class Meta:
        model = EgresadosAnexoDetalle
        exclude = ('egresados_anexo',)
        
    "Le agrego datos para chequear"
    def __init__(self, *args, **kwargs):
        self.egresados_anexo_id = kwargs.pop('egresados_anexo_id')
        self.max_egresados = kwargs.pop('max_egresados')
        super(EgresadosAnexoDetalleForm, self).__init__(*args, **kwargs)

    def clean_anio_ingreso(self):
        egresados = EgresadosAnexo.objects.get(pk = self.egresados_anexo_id)
        if int(self.cleaned_data['anio_ingreso']) >= egresados.anio:
            raise ValidationError("El año de ingreso debe ser menor que el año de egreso.")
            
        try:
            registro = EgresadosAnexoDetalle.objects.get(anio_ingreso = self.cleaned_data['anio_ingreso'], egresados_anexo = self.egresados_anexo_id)
        except:
            registro = None
        if registro is not None and registro.id != self.instance.id:
            raise ValidationError("Ya se detalló ese año para el año de egresados")
        return self.cleaned_data['anio_ingreso']

    def clean_cantidad_egresados(self):
        # egresados = self.instance.egresados_anexo # No lo puedo hacer así porque al crearlo no tiene instance
        egresados = EgresadosAnexo.objects.get(pk = self.egresados_anexo_id)
        egresados.get_suma_egresados_detalle()
        if self.cleaned_data['cantidad_egresados'] > egresados.cantidad_egresados:
            raise ValidationError("La cantidad de egresados es mayor que la cantidad declarada.")
        else:
            # Verificar que la suma de los detalles anteriores y el actual no sea mayor que el máximo
            suma_detalle = egresados.get_suma_egresados_detalle()
            if self.instance.id is not None: # Se está editando?
                suma_detalle -= self.instance.cantidad_egresados

            if suma_detalle is not None and (suma_detalle + self.cleaned_data['cantidad_egresados']) > egresados.cantidad_egresados:
                raise ValidationError("La suma de los egresados de todos los años es mayor que la cantidad declarada.")
                
        return self.cleaned_data['cantidad_egresados']
