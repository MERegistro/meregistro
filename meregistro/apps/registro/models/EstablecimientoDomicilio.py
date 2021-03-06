# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.TipoDomicilio import TipoDomicilio
from apps.registro.models.Localidad import Localidad
from apps.registro.models.Establecimiento import Establecimiento
from django.core.exceptions import ValidationError
from apps.seguridad.audit import audit


@audit
class EstablecimientoDomicilio(models.Model):
	
	TIPO_POSTAL = 'Postal'
	TIPO_INSTITUCIONAL = 'Institucional'
	
	establecimiento = models.ForeignKey(Establecimiento, related_name='domicilios')
	tipo_domicilio = models.ForeignKey(TipoDomicilio)
	localidad = models.ForeignKey(Localidad, related_name='domicilios_establecimientos')
	calle = models.CharField(max_length=100)
	altura = models.CharField(max_length=15)
	referencia = models.CharField(max_length=255, null=True, blank=True)
	cp = models.CharField(max_length=20)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_establecimiento_domicilio'

	def __unicode__(self):
		if self.cp:
			cp = " (CP: " + self.cp + ")"
		else:
			cp = ""
		return "%s %s - %s %s" % (self.calle, self.altura, self.localidad.nombre, cp)

	def __init__(self, *args, **kwargs):
		super(EstablecimientoDomicilio, self).__init__(*args, **kwargs)
