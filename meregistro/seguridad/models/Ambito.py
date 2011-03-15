# -*- coding: UTF-8 -*-

from django.db import models

class Ambito(models.Model):
  descripcion = models.CharField(max_length=255)
  path = models.CharField(max_length=255)
  level = models.IntegerField()

  class Meta:
    app_label = 'seguridad'
