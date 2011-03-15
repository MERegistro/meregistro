# -*- coding: UTF-8 -*-

from django.db import models

class Aplicacion(models.Model):
  nombre = models.CharField(max_length=255)
  descripcion = models.CharField(max_length=255)
  home_url = models.CharField(max_length=255)

  class Meta:
    app_label = 'seguridad'
