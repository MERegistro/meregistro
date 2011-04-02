from django.db import models
from django import forms
from meregistro.registro.models import DependenciaFuncional

class Establecimiento(models.Model):
  dependencia_funcional = models.ForeignKey(DependenciaFuncional)
  cue = models.IntegerField(unique = True)
  nombre = models.CharField(max_length = 100)
  norma_creacion = models.CharField(max_length = 100, null = True, blank = True)
  observaciones = models.TextField(max_length = 255, null = True, blank = True)
  anio_creacion = models.IntegerField(null = True, blank = True)

  class Meta:
    app_label = 'registro'
