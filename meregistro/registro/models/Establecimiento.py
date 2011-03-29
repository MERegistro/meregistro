from django.db import models
from meregistro.registro.models import DependenciaFuncional, Jurisdiccion

class Establecimiento(models.Model):
  dependencia_funcional = models.ForeignKey(DependenciaFuncional)
  cue = models.IntegerField(unique=True)
  nombre = models.CharField(max_length=100)
  norma_creacion = models.CharField(max_length=100, null=True)
  observaciones = models.CharField(max_length=255)
  anio_creacion = models.IntegerField(null = True)

  class Meta:
    app_label = 'registro'
