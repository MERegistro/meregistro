# -*- coding: utf-8 -*-
from django.db import models
from apps.validez_nacional.models import Solicitud
"""
Informe de Solicitud de validez de Título nacional
"""
class InformeSolicitud(models.Model):

    solicitud = models.ForeignKey(Solicitud, related_name='informe')
    normativa_implementacion = models.BooleanField(default=True)
    disenio_jurisdiccional_unico = models.BooleanField(default=True)
    denominacion_titulo = models.BooleanField(default=True)
    carga_horaria_minima = models.BooleanField(default=True)
    organizacion_estudios = models.BooleanField(default=True)
    organizacion_tres_campos = models.BooleanField(default=True)
    presencia_residencia_pedagogica = models.BooleanField(default=True)
    acreditacion_condiciones_institucionales = models.BooleanField(default=True)
    observaciones = models.TextField(null=True, blank=True)
    
    class Meta:
        app_label = 'validez_nacional'
        db_table = 'validez_nacional_informe_solicitud'

    def __unicode__(self):
        return 'Informe de Solicitud'
