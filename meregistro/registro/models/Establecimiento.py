from django.db import models
from meregistro.registro.models import DependenciaFuncional

class Establecimiento(models.Model):
  dependencia_funcional = models.ForeignKey(DependenciaFuncional)
  cue = models.IntegerField(unique=True)
  nombre = models.CharField(max_length=100)
  norma_creacion = models.CharField(max_length=100)
  obs = models.CharField(max_length=255)
    
  class Meta:
    app_label = 'registro'
