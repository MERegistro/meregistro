# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models import Anexo
from apps.postitulos.models import Solicitud, ValidezNacional
import datetime
	

class SolicitudAnexo(models.Model):
	anexo = models.ForeignKey(Anexo, related_name='anexo_solicitudes_postitulo')
	solicitud = models.ForeignKey(Solicitud, related_name='anexos_postitulo')

	class Meta:
		app_label = 'postitulos'
		db_table = 'postitulos_solicitud_anexos'
		unique_together = ('anexo', 'solicitud')


	def __unicode__(self):
		return str(self.anexo) + ' - ' + str(self.solicitud)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(SolicitudAnexo, self).__init__(*args, **kwargs)


	def registro_validez_nacional(self):
		return ValidezNacional.objects.get(tipo_unidad_educativa=ValidezNacional.TIPO_UE_Anexo, unidad_educativa_id=self.id)
