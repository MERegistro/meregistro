# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models import Solicitud, ValidezNacional
from apps.registro.models import Establecimiento
import datetime
	

class SolicitudEstablecimiento(models.Model):
	establecimiento = models.ForeignKey(Establecimiento, related_name='establecimiento_solicitudes_postitulo')
	solicitud = models.ForeignKey(Solicitud, related_name='establecimientos_postitulo')

	class Meta:
		app_label = 'postitulos'
		db_table = 'postitulos_solicitud_establecimientos'
		unique_together = ('establecimiento', 'solicitud')


	def registro_validez_nacional(self):
		return ValidezNacional.objects.get(tipo_unidad_educativa=ValidezNacional.TIPO_UE_SEDE, unidad_educativa_id=self.id)
