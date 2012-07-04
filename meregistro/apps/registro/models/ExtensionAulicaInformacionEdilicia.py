# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.Nivel import Nivel
from apps.seguridad.audit import audit

#@audit
class ExtensionAulicaInformacionEdilicia(models.Model):
    extension_aulica = models.ForeignKey(ExtensionAulica)
    tipo_dominio = models.ForeignKey(TipoDominio, null = True)
    tipo_compartido = models.ForeignKey(TipoCompartido, null = True, blank = True)
    niveles = models.ManyToManyField(Nivel, null = True, blank = True, db_table = 'registro_extension_aulica_edificio_compartido_niveles')

    class Meta:
        app_label = 'registro'
        db_table = 'registro_extension_aulica_informacion_edilicia'


