# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.seguridad.models.Usuario import Usuario
from apps.seguridad.audit import audit


@audit
class AnexoCertificacionCarga(models.Model):
    anexo = models.ForeignKey(Anexo, related_name='certificacion_carga')
    anio = models.IntegerField()
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario)

    class Meta:
        app_label = 'registro'
        unique_together = ('anexo', 'anio')
        db_table = 'registro_anexo_certificacion_carga'    
