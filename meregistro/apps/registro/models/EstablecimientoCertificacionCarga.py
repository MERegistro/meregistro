# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.seguridad.models.Usuario import Usuario
from apps.seguridad.audit import audit


@audit
class EstablecimientoCertificacionCarga(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, related_name='certificacion_carga')
    anio = models.IntegerField()
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario)

    class Meta:
        app_label = 'registro'
        unique_together = ('establecimiento', 'anio')
        db_table = 'registro_establecimiento_certificacion_carga'    
