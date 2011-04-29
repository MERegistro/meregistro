# -*- coding: utf-8 -*-
from django.db import models
from registro.models import Anexo, Estado

class AnexoEstado(models.Model):
	anexo = models.ForeignKey(Anexo)
	estado = models.ForeignKey(Estado)
	fecha = models.DateField()

	class Meta:
		app_label = 'registro'
		#db_table = 'registro_anexos_estados'

	def __unicode__(self):
		return self.estado.nombre

