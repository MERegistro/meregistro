from django.db import models
from meregistro.apps.registro.models.Region import Region
from meregistro.apps.seguridad.models import Ambito


class Jurisdiccion(models.Model):
    prefijo = models.IntegerField(null=True)
    region = models.ForeignKey(Region)
    nombre = models.CharField(max_length=50)
    ambito = models.ForeignKey(Ambito, editable=False, null=True)

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
            self.ambito = Ambito.objects.get(level=0).createChild(self.nombre)
        else:
            self.ambito.descripcion = self.nombre
            self.ambito.save()
