# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import EgresadosAnexo



class EgresadosAnexoForm(forms.ModelForm):

    ANIOS_CHOICES = [('', '-------')] + [(i, i) for i in range(1980, 2021)]

    anio = forms.ChoiceField(label = 'Año', choices = ANIOS_CHOICES, required = True)
    cantidad_egresados = forms.IntegerField(required = True, min_value = 1)
    

    class Meta:
        model = EgresadosAnexo
        exclude = ('anexo', 'titulo_jurisdiccional',)
        
    "Le agrego datos para chequear"
    def __init__(self, *args, **kwargs):
        self.anexo_id = kwargs.pop('anexo_id')
        self.titulo_jurisdiccional_id = kwargs.pop('titulo_jurisdiccional_id')
        super(EgresadosAnexoForm, self).__init__(*args, **kwargs)

    def clean_anio(self):
        try:
            registro = EgresadosAnexo.objects.get(anio = self.cleaned_data['anio'], anexo = self.anexo_id, titulo_jurisdiccional = self.titulo_jurisdiccional_id)
        except:
            registro = None
        if registro is not None and registro.id != self.instance.id:
            raise ValidationError("El título ya tiene egresados en este año")
        return self.cleaned_data['anio']
