# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.UnidadExtension import UnidadExtension
from apps.registro.models.EstadoUnidadExtension import EstadoUnidadExtension


class UnidadExtensionEstado(models.Model):
    unidad_extension = models.ForeignKey(UnidadExtension)
    estado = models.ForeignKey(EstadoUnidadExtension)
    fecha = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_unidad_extension_estados'

    def __unicode__(self):
        return self.estado.nombre
