# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccional
from apps.titulos.models import Titulo
from apps.titulos.forms import TituloJurisdiccionalForm


class TituloJurisdiccionalDatosBasicosForm(forms.ModelForm):
    #titulo = forms.ModelChoiceField(label = 'Título', choices = choices, required = True)  -> No funciona, arroja que la opción elegida no es válida

    class Meta:
       model = TituloJurisdiccional
       fields = ('tipo_titulo', 'titulo')
