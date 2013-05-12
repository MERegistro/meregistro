# -*- coding: utf-8 -*-

from django.db import models
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.registro.models.DependenciaFuncional import DependenciaFuncional
	
class UnidadEducativa(models.Model):
	cue = models.CharField(max_length=9, unique=True)
	nombre = models.CharField(max_length=255)
	tipo_unidad_educativa = models.CharField(max_length=20)
	jurisdiccion = models.ForeignKey(Jurisdiccion, editable=False, null=True)
	dependencia_funcional = models.ForeignKey(DependenciaFuncional, editable=False, null=True)

	class Meta:
		app_label = 'consulta_validez'
		ordering = ['nombre']
		
	def __unicode__(self):
		return self.cue + " - " + self.nombre

class Titulo(models.Model):
	unidad_educativa = models.ForeignKey(UnidadEducativa, null=True)
	denominacion = models.CharField(max_length=255)
	primera = models.CharField(max_length=255)
	ultima = models.CharField(max_length=255)
	nroinfd = models.CharField(max_length=255)
	carrera = models.CharField(max_length=255)
	normativa_jurisdiccional = models.CharField(max_length=255)
	normativa_nacional = models.CharField(max_length=255)

	class Meta:
		app_label = 'consulta_validez'

