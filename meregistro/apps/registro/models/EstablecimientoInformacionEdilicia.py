# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.Nivel import Nivel
from apps.seguridad.audit import audit

@audit
class EstablecimientoInformacionEdilicia(models.Model):
    establecimiento = models.ForeignKey(Establecimiento)
    tipo_dominio = models.ForeignKey(TipoDominio, null = True)
    tipo_compartido = models.ForeignKey(TipoCompartido, null = True, blank = True)
    niveles = models.ManyToManyField(Nivel, null = True, blank = True, db_table = 'registro_establecimiento_edificio_compartido_niveles')

    class Meta:
        app_label = 'registro'
        db_table = 'registro_establecimiento_informacion_edilicia'


