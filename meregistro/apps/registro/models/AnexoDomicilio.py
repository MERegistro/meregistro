# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.TipoDomicilio import TipoDomicilio
from apps.registro.models.Localidad import Localidad
from apps.registro.models.Anexo import Anexo
from django.core.exceptions import ValidationError
from apps.seguridad.audit import audit

@audit
class AnexoDomicilio(models.Model):
	
	TIPO_POSTAL = 'Postal'
	TIPO_INSTITUCIONAL = 'Institucional'
	
	anexo = models.ForeignKey(Anexo, related_name = 'anexo_domicilio')
	tipo_domicilio = models.ForeignKey(TipoDomicilio)
	localidad = models.ForeignKey(Localidad, related_name = 'anexo_localidad')
	calle = models.CharField(max_length=100)
	altura = models.CharField(max_length=15)
	referencia = models.CharField(max_length=255, null=True, blank=True)
	cp = models.CharField(max_length=20)

	class Meta:
		app_label = 'registro'
		db_table = 'registro_anexo_domicilio'

	def __unicode__(self):
		if self.cp:
			cp = u" (CP: " + self.cp + ")"
		else:
			cp = u""
		return u"%s %s - %s %s" % (self.calle, self.altura, self.localidad.nombre, cp)

	def __init__(self, *args, **kwargs):
		super(AnexoDomicilio, self).__init__(*args, **kwargs)
