# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.TipoDomicilio import TipoDomicilio
from meregistro.registro.models.Localidad import Localidad
from meregistro.registro.models.Anexo import Anexo
from django.core.exceptions import ValidationError

class AnexoDomicilio(models.Model):
	anexo = models.ForeignKey(Anexo)
	tipo_domicilio = models.ForeignKey(TipoDomicilio)
	localidad = models.ForeignKey(Localidad, related_name = "anexos_domicilios")
	calle = models.CharField(max_length = 100)
	altura = models.CharField(max_length = 5)
	referencia = models.CharField(max_length = 255)
	#cp = models.CharField(max_length = 50)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_anexo_domicilio'

	def __unicode__(self):
		return str(self.calle) + str(self.altura)

	def __init__(self, *args, **kwargs):
		super(AnexoDomicilio, self).__init__(*args, **kwargs)
