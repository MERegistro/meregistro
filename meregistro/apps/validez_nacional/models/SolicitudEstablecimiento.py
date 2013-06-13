# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud
from apps.registro.models import Establecimiento
import datetime
	

class SolicitudEstablecimiento(models.Model):
	establecimiento = models.ForeignKey(Establecimiento, related_name='solicitudes')
	solicitud = models.ForeignKey(Solicitud, related_name='establecimientos')

	class Meta:
		app_label = 'validez_nacional'
		db_table = 'validez_nacional_solicitud_establecimientos'
		unique_together = ('establecimiento', 'solicitud')
