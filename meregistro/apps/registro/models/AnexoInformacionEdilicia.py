# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.Nivel import Nivel
from apps.seguridad.audit import audit

@audit
class AnexoInformacionEdilicia(models.Model):
    anexo = models.ForeignKey(Anexo)
    tipo_dominio = models.ForeignKey(TipoDominio, null = True)
    tipo_compartido = models.ForeignKey(TipoCompartido, null = True, blank = True)
    niveles = models.ManyToManyField(Nivel, null = True, blank = True, db_table = 'registro_anexo_edificio_compartido_niveles')

    class Meta:
        app_label = 'registro'
        db_table = 'registro_anexo_informacion_edilicia'


