# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.TipoNormativa import TipoNormativa
from meregistro.registro.models.Jurisdiccion import Jurisdiccion
from meregistro.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from meregistro.registro.models.DependenciaFuncional import DependenciaFuncional
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import datetime
from meregistro.seguridad.models import Ambito

YEARS_CHOICES = tuple((int(n), str(n)) for n in range(1800, datetime.datetime.now().year + 1))

class Establecimiento(models.Model):
	dependencia_funcional = models.ForeignKey(DependenciaFuncional)
	cue = models.CharField(max_length = 5)
	nombre = models.CharField(max_length = 255)
	tipo_normativa = models.ForeignKey(TipoNormativa)
	unidad_academica = models.BooleanField()
	nombre_unidad_academica = models.CharField(max_length = 100, null = True, blank = True)
	norma_creacion = models.CharField(max_length = 100)
	observaciones = models.TextField(max_length = 255, null = True, blank = True)
	anio_creacion = models.IntegerField(null = True, blank = True, choices = YEARS_CHOICES)
	telefono = models.CharField(max_length = 100, null = True, blank = True)
	email = models.EmailField(max_length = 255, null = True, blank = True)
	sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)
	ambito = models.ForeignKey(Ambito, editable=False)

	class Meta:
		app_label = 'registro'
		ordering = ['nombre']

	def __unicode__(self):
		return self.nombre

	def clean(self):
		#Chequea que la combinación entre jurisdiccion y cue sea única
		try:
			est = Establecimiento.objects.get(cue = self.cue, dependencia_funcional__jurisdiccion__id = self.dependencia_funcional.jurisdiccion.id)
			if est and est != self:
				raise ValidationError('Ya existe un establecimiento con ese CUE en su jurisdicción.')
		except ObjectDoesNotExist:
			pass

	def registrar_estado(self, estado):
		registro = RegistroEstablecimiento(estado = estado)
		registro.fecha_solicitud = datetime.date.today()
		registro.establecimiento_id = 1
		registro.save()

	def save(self):
		self.updateAmbito()
		models.Model.save(self)

	def updateAmbito(self):
		if self.pk is None or self.ambito is None:
			self.ambito = self.dependencia_funcional.ambito.createChild(self.nombre)
		else:
			self.ambito.descripcion = self.nombre
			self.ambito.save()
