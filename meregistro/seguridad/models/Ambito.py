# -*- coding: UTF-8 -*-

from django.db import models

class Ambito(models.Model):
  descripcion = models.CharField(max_length=255)
  parentPath = models.CharField(max_length=255)
  level = models.IntegerField()
  parent = models.ForeignKey('self', null=True)

  class Meta:
    app_label = 'seguridad'

  def __unicode__(self):
    return self.descripcion

  def createChild(self, childDescripcion):
    child = Ambito()
    child.descripcion = childDescripcion
    child.level = self.level + 1
    child.parentPath = self.parentPath + str(self.id) + '/'
    child.parent = self
    child.save()
    return child
