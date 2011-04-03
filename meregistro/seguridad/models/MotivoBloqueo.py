# -*- coding: UTF-8 -*-

from django.db import models

class MotivoBloqueo(models.Model):
  descripcion = models.CharField(max_length=255)
  
  class Meta:
    app_label = 'seguridad'

