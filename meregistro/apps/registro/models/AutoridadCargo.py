from django.db import models


class AutoridadCargo(models.Model):
  descripcion = models.CharField(max_length=50, unique=True)

  class Meta:
    app_label = 'registro'
    db_table = 'registro_autoridad_cargo'
    ordering = ['descripcion']

  def __unicode__(self):
    return self.descripcion

  def delete(self):
    if (self.anexoautoridad_set.count() > 0
      or self.establecimientoautoridad_set.count() > 0
      or self.extensionaulicaautoridad_set.count() > 0):
      raise Exception('Entidad en uso')
    models.Model.delete(self)
