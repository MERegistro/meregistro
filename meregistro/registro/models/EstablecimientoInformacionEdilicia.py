# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.Establecimiento import Establecimiento
from meregistro.registro.models.TipoDominio import TipoDominio
from meregistro.registro.models.TipoCompartido import TipoCompartido
from meregistro.registro.models.Nivel import Nivel

class EstablecimientoInformacionEdilicia(models.Model):
    establecimiento = models.ForeignKey(Establecimiento)
    tipo_dominio = models.ForeignKey(TipoDominio, null = True)
    tipo_compartido = models.ForeignKey(TipoCompartido, null = True, blank = True)
    niveles = models.ManyToManyField(Nivel, null = True, blank = True, db_table = 'registro_establecimiento_edificio_compartido_niveles')

    class Meta:
        app_label = 'registro'
        db_table = 'registro_establecimiento_informacion_edilicia'


