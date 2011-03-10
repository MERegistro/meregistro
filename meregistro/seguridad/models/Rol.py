# -*- coding: UTF-8 -*-

from django.db import models

class Rol(models.Model):
  nombre = models.CharField(max_length=40)
  descripcion = models.CharField(max_length=255)
  
  class Meta:
    app_label = 'seguridad'
