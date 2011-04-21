# -*- coding: utf-8 -*-
from django.forms import ModelForm
from registro.models import Establecimiento
from django.core.exceptions import ValidationError

class EstablecimientoForm(ModelForm):

	class Meta:
		model = Establecimiento

	def clean_anio_creacion(self):
		anio_creacion = self.cleaned_data['anio_creacion']
		try:
			if(anio_creacion is not None):
				anio_creacion = int(anio_creacion)
		except ValidationError:
			pass
		return anio_creacion
