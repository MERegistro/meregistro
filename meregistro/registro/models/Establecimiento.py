# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models import DependenciaFuncional, TipoNormativa, Jurisdiccion
from django.core.exceptions import ValidationError

class Establecimiento(models.Model):
	dependencia_funcional = models.ForeignKey(DependenciaFuncional)
	cue = models.CharField(max_length = 10)
	nombre = models.CharField(max_length = 255)
	tipo_normativa = models.ForeignKey(TipoNormativa)
	unidad_academica = models.BooleanField()
	nombre_unidad_academica = models.CharField(max_length = 100, null = True, blank = True)
	norma_creacion = models.CharField(max_length = 100)
	observaciones = models.TextField(max_length = 255, null = True, blank = True)
	anio_creacion = models.IntegerField(null = True, blank = True)
	telefono = models.CharField(max_length = 100, null = True, blank = True)
	email = models.EmailField(max_length = 255, null = True, blank = True)
	sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)

	class Meta:
		app_label = 'registro'

	def __unicode__(self):
		return self.nombre

	def clean(self):
		#Chequea que la combinación entre prefijo y cue sea única
		try:
			est = Establecimiento.objects.get(cue = self.cue, dependencia_funcional__jurisdiccion__prefijo__exact = self.dependencia_funcional.jurisdiccion.prefijo)
			if est and est != self:
				raise ValidationError('Ya existe un establecimiento con ese CUE en su jurisdicción.')
		except Establecimiento.DoesNotExist:
			pass
