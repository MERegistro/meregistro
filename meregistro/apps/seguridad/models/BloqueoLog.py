# -*- coding: UTF-8 -*-

from django.db import models
from apps.seguridad.models import Usuario, MotivoBloqueo
from apps.seguridad.audit import audit

@audit
class BloqueoLog(models.Model):
    usuario = models.ForeignKey(Usuario)
    motivo = models.ForeignKey(MotivoBloqueo)
    fecha = models.DateField()

    class Meta:
        app_label = 'seguridad'
        db_table = 'seguridad_bloqueo_log'
