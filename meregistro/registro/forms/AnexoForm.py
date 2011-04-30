# -*- coding: utf-8 -*-
from django.forms import ModelForm
from registro.models import Anexo
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime
import time

currentYear = datetime.datetime.now().year

class AnexoForm(ModelForm):
	fecha_alta = forms.DateField(input_formats = ['%d/%m/%Y', '%d/%m/%y'], required = False, initial = datetime.date.today)

	# TODO: investigar, el widget se resetea si la fecha no es válida
	#fecha_alta = forms.DateField(required = False, initial = datetime.date.today, widget = SelectDateWidget(years = range(1900, currentYear + 5)))

	class Meta:
		model = Anexo

	def clean_cue(self):
		cue = self.cleaned_data['cue']
		try:
			if int(cue) <= 0:
				raise ValidationError(u'El CUE tiene que ser mayor a cero.')
		except ValueError:
			raise ValidationError(u'Ingrese un valor numérico.')
		if int(cue) < 10 and len(cue) < 2:
			cue = u'0' + str(cue) # 03...08...09
		return cue