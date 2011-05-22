from django.db import models
from meregistro.registro.models.Jurisdiccion import Jurisdiccion


class Departamento(models.Model):
    jurisdiccion = models.ForeignKey(Jurisdiccion)
    nombre = models.CharField(max_length=50)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']
        unique_together = ('jurisdiccion', 'nombre')

    def __unicode__(self):
        return self.nombre
