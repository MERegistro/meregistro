# -*- coding: utf-8 -*-
from django.db import models
from meregistro.apps.registro.models.UnidadExtension import UnidadExtension
from meregistro.apps.registro.models.Estado import Estado


class UnidadExtensionEstado(models.Model):
    unidad_extension = models.ForeignKey(UnidadExtension)
    estado = models.ForeignKey(Estado)
    fecha = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_unidad_extension_estado'

    def __unicode__(self):
        return self.estado.nombre
