# -*- coding: UTF-8 -*-

from django.db import models

class TipoDocumento(models.Model):
  descripcion = models.CharField(max_length=50)
  abreviatura = models.CharField(max_length=5)
  
  class Meta:
    app_label = 'seguridad'

  def __unicode__(self):
    return self.descripcion
