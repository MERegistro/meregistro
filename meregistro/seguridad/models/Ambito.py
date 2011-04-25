# -*- coding: UTF-8 -*-

from django.db import models

class Ambito(models.Model):
  descripcion = models.CharField(max_length=255)
  path = models.CharField(max_length=255)
  level = models.IntegerField()
  parent = models.ForeignKey('self', null=True)

  class Meta:
    app_label = 'seguridad'

  def __unicode__(self):
    s = self.descripcion
    parent = self.parent
    while parent is not None:
      s = parent.descripcion + '-' + s
      parent = parent.parent
    return s

  def createChild(self, childDescripcion):
    child = Ambito()
    child.descripcion = childDescripcion
    child.level = self.level + 1
    child.parent = self
#    child.path = self.path + '/'
    child.save()
    child.path = self.path + '/' + str(child.id)
    child.save()
    return child
