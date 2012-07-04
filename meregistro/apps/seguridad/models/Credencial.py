# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Aplicacion


class Credencial(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    aplicacion = models.ForeignKey(Aplicacion, related_name='credenciales')
    grupo = models.CharField(max_length=255)
    credenciales_hijas = models.ManyToManyField('self', related_name='credenciales_padres', symmetrical=False)

    class Meta:
        app_label = 'seguridad'

    def __unicode__(self):
        return self.descripcion
