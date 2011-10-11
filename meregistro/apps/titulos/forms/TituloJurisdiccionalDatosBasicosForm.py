# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccional
from apps.titulos.forms import TituloJurisdiccionalForm


class TituloJurisdiccionalDatosBasicosForm(forms.ModelForm):
    titulo = forms.ChoiceField(label = 'Título', choices = [], required = True)

    class Meta:
       model = TituloJurisdiccional
       fields = ('tipo_titulo', 'titulo')
