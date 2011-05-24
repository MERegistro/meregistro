# -*- coding: utf-8 -*-
from django.db import models
from meregistro.registro.models.Anexo import Anexo
from meregistro.registro.models.Estado import Estado


class AnexoEstado(models.Model):
    anexo = models.ForeignKey(Anexo)
    estado = models.ForeignKey(Estado)
    fecha = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_anexo_estado'

    def __unicode__(self):
        return self.estado.nombre
