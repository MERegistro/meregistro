# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models import Establecimiento
from apps.validez_nacional.models import Solicitud
import datetime
	

class SolicitudEstablecimiento(models.Model):
	establecimiento = models.ForeignKey(Establecimiento, related_name='solicitudes')
	solicitud = models.ForeignKey(Solicitud, related_name='establecimientos')

	class Meta:
		app_label = 'validez_nacional'
		db_table = 'validez_nacional_solicitud_establecimientos'
		unique_together = ('establecimiento', 'solicitud')


	def __unicode__(self):
		return str(self.establecimiento) + ' - ' + str(self.solicitud)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(SolicitudEstablecimiento, self).__init__(*args, **kwargs)
