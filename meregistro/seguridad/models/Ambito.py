# -*- coding: UTF-8 -*-

from django.db import models

class Ambito(models.Model):
  descripcion = models.CharField(max_length=255)
  parent = models.ForeignKey('self', null=True)
  level = models.IntegerField()

  class Meta:
    app_label = 'seguridad'

  def __unicode__(self):
    return self.descripcion
