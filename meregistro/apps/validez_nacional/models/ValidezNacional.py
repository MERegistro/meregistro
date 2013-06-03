# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud
import datetime

"""
Título nacional Validado por el INFOD
"""
class ValidezNacional(models.Model):
	
	TIPO_UE_SEDE = u'Sede'
	TIPO_UE_ANEXO = u'Anexo'

	solicitud = models.ForeignKey(Solicitud, null=False)
	nro_infd = models.CharField(max_length=99, null=False)
	cue = models.CharField(max_length=9, null=False, db_index=True)
	tipo_unidad_educativa = models.CharField(max_length=10, null=False)
	unidad_educativa_id = models.PositiveIntegerField(null=False)

	class Meta:
		app_label = 'validez_nacional'
		db_table = 'validez_nacional_validez_nacional'

	def __unicode__(self):
		return self.titulo.nombre

	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(Solicitud, self).__init__(*args, **kwargs)
		self.estados = self.get_estados()

	"Sobreescribo para eliminar los objetos relacionados"
	def delete(self, *args, **kwargs):
		for normativa in self.normativas.all():
			normativa.delete()
		for est in self.estados.all():
			est.delete()
		super(Solicitud, self).delete(*args, **kwargs)

	def registrar_estado(self):
		from apps.validez_nacional.models import SolicitudEstado
		registro = SolicitudEstado(estado=self.estado)
		registro.fecha = datetime.date.today()
		registro.solicitud_id = self.id
		registro.save()

	def get_estados(self):
		from apps.titulos.models import SolicitudEstado
		try:
			estados = SolicitudEstado.objects.filter(solicitud=self).order_by('fecha', 'id')
		except:
			estados = {}
		return estados
