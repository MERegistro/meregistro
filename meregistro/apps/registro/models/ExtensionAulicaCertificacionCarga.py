# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.seguridad.models.Usuario import Usuario
from apps.seguridad.audit import audit


@audit
class ExtensionAulicaCertificacionCarga(models.Model):
    extension_aulica = models.ForeignKey(ExtensionAulica, related_name='certificacion_carga')
    anio = models.IntegerField()
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario)

    class Meta:
        app_label = 'registro'
        unique_together = ('extension_aulica', 'anio')
        db_table = 'registro_extension_aulica_certificacion_carga'    
