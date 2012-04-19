# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.Turno import Turno
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.Nivel import Nivel
from apps.seguridad.audit import audit

@audit
class ExtensionAulicaTurno(models.Model):
    extension_aulica = models.ForeignKey(ExtensionAulica)
    turno = models.ForeignKey(Turno)
    tipo_dominio = models.ForeignKey(TipoDominio, null=True)  # exclusivo, compartido
    tipo_compartido = models.ForeignKey(TipoCompartido, null=True, blank=True)  # Otra institución, etc
    niveles = models.ManyToManyField(Nivel, null=True, blank=True, db_table='registro_extension_aulica_turno_niveles')

    class Meta:
        app_label = 'registro'
        unique_together = ('extension_aulica', 'turno')
        db_table = 'registro_extension_aulica_turno'


