# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Credencial


class Rol(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=255)
    credenciales = models.ManyToManyField(Credencial, related_name='roles')
    roles_asignables = models.ManyToManyField('self', related_name='roles_asignadores', symmetrical=False)

    class Meta:
        app_label = 'seguridad'

    def __unicode__(self):
        return self.descripcion
