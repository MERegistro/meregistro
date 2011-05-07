# -*- coding: UTF-8 -*-

from django.db import models

class MotivoBloqueo(models.Model):
  ACCION_CHOICES = (
    (u'L', u'Bloqueo'),
    (u'U', u'Desbloqueo'),
  )
  accion = models.CharField(max_length=2, choices=ACCION_CHOICES)
  descripcion = models.CharField(max_length=255)

  class Meta:
    app_label = 'seguridad'
    db_table = 'seguridad_motivo_bloqueo'

  def __unicode__(self):
    return self.descripcion
