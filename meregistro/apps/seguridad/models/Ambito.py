# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import TipoAmbito

class Ambito(models.Model):
    
    TIPO_SUPERIOR = 'Superior'
    TIPO_JURISDICCION = 'Jurisdiccion'
    TIPO_DEPENDENCIA_FUNCIONAL = 'DependenciaFuncional'
    TIPO_ESTABLECIMIENTO = 'Sede'
    TIPO_ANEXO = 'Anexo'
    TIPO_EXTENSION_AULICA = 'ExtensionAulica'

    descripcion = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    level = models.IntegerField()
    parent = models.ForeignKey('self', null=True)
    vigente = models.BooleanField(default=True)
    tipo = models.ForeignKey(TipoAmbito)

    class Meta:
        app_label = 'seguridad'

    def __unicode__(self):
        s = self.descripcion
        return s

    def createChild(self, childDescripcion, model):
        child = Ambito()
        child.descripcion = childDescripcion
        child.level = self.level + 1
        child.parent = self
        print "tipo:", TipoAmbito.get_tipo_by_model(model)
        child.tipo = TipoAmbito.get_tipo_by_model(model)
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
