# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.registro.models.EstadoAnexo import EstadoAnexo


class AnexoEstado(models.Model):
    anexo = models.ForeignKey(Anexo)
    estado = models.ForeignKey(EstadoAnexo)
    fecha = models.DateField()

    class Meta:
        app_label = 'registro'
        db_table = 'registro_anexo_estados'

    def __unicode__(self):
        return self.estado.nombre
