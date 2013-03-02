# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteEstablecimiento import CohorteEstablecimiento
import datetime

"Seguimiento de cada cohorte del establecimiento"
class CohorteEstablecimientoSeguimiento(models.Model):
	cohorte_establecimiento = models.ForeignKey(CohorteEstablecimiento, related_name='seguimiento')
	anio = models.PositiveIntegerField()
	solo_cursan_nuevas_unidades = models.PositiveIntegerField()
	solo_recursan_nuevas_unidades = models.PositiveIntegerField()
	recursan_cursan_nuevas_unidades = models.PositiveIntegerField()
	no_cursan = models.PositiveIntegerField()
	egresados = models.PositiveIntegerField()
	observaciones = models.CharField(max_length=255, null=True, blank=True)


	class Meta:
		app_label = 'titulos'
		ordering = ['cohorte_establecimiento__cohorte__anio', 'anio']
		db_table = 'titulos_cohorte_establecimiento_seguimiento'
		unique_together = ('cohorte_establecimiento', 'anio') #-> no funciona, valido a mano


	def __unicode__(self):
		return str(self.anio)


	"Sobreescribo el init para agregarle propiedades"
	def __init__(self, *args, **kwargs):
		super(CohorteEstablecimientoSeguimiento, self).__init__(*args, **kwargs)


