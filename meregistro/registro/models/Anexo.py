# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models import Establecimiento
from django.core.exceptions import ValidationError

class Anexo(models.Model):
	establecimiento = models.ForeignKey(Establecimiento)
	cue = models.CharField(max_length = 2)
	fecha_alta = models.DateField(null = True, blank = True)
	nombre = models.CharField(max_length = 255)
	telefono = models.CharField(max_length = 100, null = True, blank = True)
	email = models.EmailField(max_length = 255, null = True, blank = True)
	sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)

	class Meta:
		app_label = 'registro'

	def __unicode__(self):
		return self.nombre

	def clean(self):
		# Chequea que la combinación entre establecimiento y cue sea único
		cue = self.cue
		establecimiento = self.establecimiento_id
		if cue and establecimiento:
			try:
				anexo = Anexo.objects.get(cue = self.cue, establecimiento__cue__exact = self.establecimiento.cue)
				if anexo and anexo != self:
					raise ValidationError('Ya existe un anexo con ese CUE en ese establecimiento.')
			except Anexo.DoesNotExist:
				pass

