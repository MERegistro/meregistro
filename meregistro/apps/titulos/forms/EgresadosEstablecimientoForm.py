# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import EgresadosEstablecimiento



class EgresadosEstablecimientoForm(forms.ModelForm):

    ANIOS_CHOICES = [('', '-------')] + [(i, i) for i in range(1980, 2021)]

    anio = forms.ChoiceField(label = 'Año', choices = ANIOS_CHOICES, required = True)
    cantidad_egresados = forms.IntegerField(required = True, min_value = 1)
    

    class Meta:
        model = EgresadosEstablecimiento
        exclude = ('establecimiento', 'titulo_jurisdiccional',)
        
    "Le agrego datos para chequear"
    def __init__(self, *args, **kwargs):
        self.establecimiento_id = kwargs.pop('establecimiento_id')
        self.titulo_jurisdiccional_id = kwargs.pop('titulo_jurisdiccional_id')
        super(EgresadosEstablecimientoForm, self).__init__(*args, **kwargs)

    def clean_anio(self):
        try:
            registro = EgresadosEstablecimiento.objects.get(anio = self.cleaned_data['anio'], establecimiento = self.establecimiento_id, titulo_jurisdiccional = self.titulo_jurisdiccional_id)
        except:
            registro = None
        if registro is not None and registro.id != self.instance.id:
            raise ValidationError("El título ya tiene egresados en este año")
        return self.cleaned_data['anio']
