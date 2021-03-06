# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento


class RegistroEstablecimiento(models.Model):
    establecimiento = models.ForeignKey('Establecimiento')
    estado = models.ForeignKey('EstadoEstablecimiento')
    fecha = models.DateField(null = False, blank = False, editable = False)
    observaciones = models.TextField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'registro'
        db_table = 'registro_registro_establecimiento'

    def __unicode__(self):
        return self.estado.nombre
