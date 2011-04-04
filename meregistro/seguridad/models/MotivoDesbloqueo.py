# -*- coding: UTF-8 -*-

from django.db import models

class MotivoDesbloqueo(models.Model):
  descripcion = models.CharField(max_length=255)
  
  class Meta:
    app_label = 'seguridad'

