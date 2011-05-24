# -*- coding: UTF-8 -*-

from django.db import models
from meregistro.seguridad.models import Aplicacion


class Credencial(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255)
    aplicacion = models.ForeignKey(Aplicacion, related_name='credenciales')

    class Meta:
        app_label = 'seguridad'
