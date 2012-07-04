# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TipoTitulo, Titulo, TituloJurisdiccional, EstadoTitulo
from apps.titulos.forms import TituloJurisdiccionalForm


class TituloJurisdiccionalDatosBasicosForm(forms.ModelForm):
    tipo_titulo = forms.ModelChoiceField(queryset = TipoTitulo.objects.order_by('nombre'), label = 'Tipo de título', required = True)
    titulo = forms.ModelChoiceField(queryset = Titulo.objects.order_by('nombre'), label = 'Tipo de título', required = True)
    
    class Meta:
       model = TituloJurisdiccional
       fields = ('tipo_titulo', 'titulo')

    def __init__(self, *args, **kwargs):
        self.jurisdiccion_id = kwargs.pop('jurisdiccion_id')
        super(TituloJurisdiccionalDatosBasicosForm, self).__init__(*args, **kwargs)
        "Para no cargar quichicientosmil"
        self.fields['titulo'].queryset = self.fields['titulo'].queryset.filter(jurisdicciones__id = self.jurisdiccion_id, estado__nombre = EstadoTitulo.VIGENTE)
