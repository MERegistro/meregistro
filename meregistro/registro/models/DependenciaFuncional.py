from django.db import models
from meregistro.registro.models import Jurisdiccion, GestionJurisdiccion, TipoGestion, TipoDependenciaFuncional

class DependenciaFuncional(models.Model):
  jurisdiccion = models.ForeignKey(Jurisdiccion)
  gestion_jurisdiccion = models.ForeignKey(GestionJurisdiccion)
  tipo_gestion = models.ForeignKey(TipoGestion)
  tipo_dependencia = models.ForeignKey(TipoDependenciaFuncional)
  nombre = models.CharField(max_length=50)

  class Meta:
    app_label = 'registro'

  def __str__(self):
    return self.nombre
