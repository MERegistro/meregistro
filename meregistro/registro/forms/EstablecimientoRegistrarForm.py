# -*- coding: utf-8 -*-
from django.forms import ModelForm
from registro.models import Establecimiento
from django.core.exceptions import ValidationError
from meregistro.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime


class EstablecimientoRegistrarForm(ModelForm):
	fecha_registro = forms.DateField(input_formats = ['%d/%m/%Y', '%d/%m/%y'], required = False, initial = datetime.date.today)

	class Meta:
		model = RegistroEstablecimiento

