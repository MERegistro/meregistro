# -*- coding: UTF-8 -*-

from django.db import models


class Ambito(models.Model):
    descripcion = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    level = models.IntegerField()
    parent = models.ForeignKey('self', null=True)
    vigente = models.BooleanField(default=True)

    class Meta:
        app_label = 'seguridad'

    def __unicode__(self):
        s = self.descripcion
        return s

    def createChild(self, childDescripcion):
        child = Ambito()
        child.descripcion = childDescripcion
        child.level = self.level + 1
        child.parent = self
        child.save()
        if self.path[-1] == '/': c = ''
        else: c = '/'
        child.path = self.path + c + str(child.id) +'/'
        child.save()
        return child


    def set_parent(self, parent):
        childs = Ambito.objects.filter(path__istartswith=self.path).filter(level=self.level+1)
        self.path = parent.path + str(self.id) +'/'
        self.level = parent.level + 1
        self.parent = parent
        self.save()
        for c in childs:
            c.set_parent(self)
            c.save()

    def delete(self, *arg, **kw):
      self.ambito_set.all().delete()
      return models.Model.delete(self)


    def esAncestro(self, ambito):
        return ambito.path.startswith(self.path)
