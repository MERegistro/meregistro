# -*- coding: utf-8 -*-
from django.db import models
from registro.models.Estado import Estado

class RegistroEstablecimiento(models.Model):

	establecimiento = models.ForeignKey('Establecimiento')
	estado = models.ForeignKey('Estado')
	fecha_solicitud = models.DateField(null = False, blank = False)
	observaciones = models.CharField(max_length = 255, null = True, blank = True)
	fecha_registro = models.DateField(null = True, blank = True)
	fecha_envio_solicitud = models.DateField(null = True, blank = True)

	class Meta:
		app_label = 'registro'

	def __unicode__(self):
		return self.estado.nombre

