# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.seguridad.audit import audit

@audit
class ExtensionAulicaEstado(models.Model):
    extension_aulica = models.ForeignKey(ExtensionAulica)
    estado = models.ForeignKey(EstadoExtensionAulica)
    fecha = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_extension_aulica_estados'

    def __unicode__(self):
        return self.estado.nombre
