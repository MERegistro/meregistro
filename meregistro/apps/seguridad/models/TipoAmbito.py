# -*- coding: UTF-8 -*-

from django.db import models

class TipoAmbito(models.Model):
    nombre = models.CharField(max_length=40)
    descripcion = models.CharField(max_length=100)

    class Meta:
        app_label = 'seguridad'

    def __unicode__(self):
        return self.descripcion
