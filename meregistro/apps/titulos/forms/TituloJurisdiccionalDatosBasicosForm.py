# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms
from apps.titulos.models import TituloJurisdiccional
from apps.titulos.forms import TituloJurisdiccionalForm


class TituloJurisdiccionalDatosBasicosForm(forms.ModelForm):

    class Meta:
       model = TituloJurisdiccional
       fields = ('nombre', 'tipo_titulo', 'titulo')
