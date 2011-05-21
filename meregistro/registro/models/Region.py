from django.db import models
from seguridad.models import Ambito

class Region(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    def __unicode__(self):
        return self.nombre
