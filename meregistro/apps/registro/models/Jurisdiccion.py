from django.db import models
from apps.registro.models.Region import Region
from apps.seguridad.models import Ambito


class Jurisdiccion(models.Model):
    prefijo = models.CharField(null = True, max_length = 3)
    region = models.ForeignKey(Region)
    nombre = models.CharField(max_length = 50)
    ambito = models.ForeignKey(Ambito, editable = False, null =True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre

    def save(self):
        self.updateAmbito()
        models.Model.save(self)

    def updateAmbito(self):
        if self.pk is None or self.ambito is None:
            self.ambito = Ambito.objects.get(level=0).createChild(self.nombre, self)
        else:
            self.ambito.descripcion = self.nombre
            self.ambito.save()

    def delete(self):
        if (self.departamento_set.count() > 0
          or self.dependenciafuncional_set.count() > 0
          or self.titulo_set.count() > 0
          or self.carrerajurisdiccional_set.count() > 0
          or self.normativajurisdiccional_set.count() > 0):
            raise Exception('Entidad en uso')
        models.Model.delete(self)
