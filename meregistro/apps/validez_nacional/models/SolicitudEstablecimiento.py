# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud, ValidezNacional
from apps.registro.models import Establecimiento
import datetime
	

class SolicitudEstablecimiento(models.Model):
	establecimiento = models.ForeignKey(Establecimiento, related_name='solicitudes')
	solicitud = models.ForeignKey(Solicitud, related_name='establecimientos')

	class Meta:
		app_label = 'validez_nacional'
		db_table = 'validez_nacional_solicitud_establecimientos'
		unique_together = ('establecimiento', 'solicitud')


	def registro_validez_nacional(self):
		return ValidezNacional.objects.get(tipo_unidad_educativa=ValidezNacional.TIPO_UE_SEDE, unidad_educativa_id=self.id)

	
	"""
	def nro_infd_calculado(self):
		cod_jur = self.establecimiento.dependencia_funcional.jurisdiccion.prefijo
		tipo_gestion = str(self.establecimiento.dependencia_funcional.tipo_gestion.id)
		unidad_educativa_id = str(self.establecimiento.id).zfill(5)
		anio = str(datetime.date.today().year)[2:]
		titulo = 'T'
		nro_infd = cod_jur + tipo_gestion + unidad_educativa_id + anio + titulo
		return nro_infd
	"""
		
	"""
	42
	Prefijo de la jurisdicción.
	1
	Tipo de Gestión: 1 para Estatal y 2 para Privada según la tabla registro_tipo_gestion. 
	Antes era 0 (Estatal) y 1 (Privada), pero nosotros migramos 1 (Estatal) y 2 (Privada). No es un problema. De última, garantiza que no se repitan los números.
	00759
	El id de la Unidad Educativa (que debe ser único para cada Sede o Anexo).
	12
	El año calendario en que se está numerando.
	T
	Una “T” que corresponde a Título.
	017177
	El id de la tabla validez_nacional_validez_nacional que será grabado en la misma en este mismo registro.
	Debería comenzar en 20000 a partir de ahora porque los datos de validez que vamos a migrar acá ya tienen id.
	"""

