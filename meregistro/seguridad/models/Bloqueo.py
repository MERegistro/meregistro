# -*- coding: UTF-8 -*-

from django.db import models
from meregistro.seguridad.models import Usuario, MotivoBloqueo, MotivoDesbloqueo

class Bloqueo(models.Model):
  usuario = models.ForeignKey(Usuario)
  motivo_bloqueo = models.ForeignKey(MotivoBloqueo)
  motivo_desbloqueo = models.ForeignKey(MotivoDesbloqueo, null=True, blank=True)
  fecha_bloqueo = models.DateField()
  fecha_desbloqueo = models.DateField(null=True, blank=True)
  
  class Meta:
    app_label = 'seguridad'

