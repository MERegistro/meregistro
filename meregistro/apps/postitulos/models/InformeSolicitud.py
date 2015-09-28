# -*- coding: utf-8 -*-
from django.db import models
from apps.postitulos.models import Solicitud
"""
Informe de Solicitud de validez de Título nacional
"""
class InformeSolicitud(models.Model):

    solicitud = models.ForeignKey(Solicitud, related_name='informe')
    denominacion_titulo = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=999, null=True)
    
    class Meta:
        app_label = 'postitulos'
        db_table = 'postitulos_informe_solicitud'

    def __unicode__(self):
        return 'Informe de Solicitud'
