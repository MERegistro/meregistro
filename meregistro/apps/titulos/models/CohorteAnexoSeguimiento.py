# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteAnexo import CohorteAnexo
import datetime

"Seguimiento de cada cohorte del anexo"
class CohorteAnexoSeguimiento(models.Model):
    cohorte_anexo = models.ForeignKey(CohorteAnexo, related_name='seguimiento')
    anio = models.PositiveIntegerField()
    solo_cursan_nuevas_unidades = models.PositiveIntegerField()
    solo_recursan_nuevas_unidades = models.PositiveIntegerField()
    recursan_cursan_nuevas_unidades = models.PositiveIntegerField()
    no_cursan = models.PositiveIntegerField()
    egresados = models.PositiveIntegerField()
    observaciones = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte_anexo__cohorte__anio', 'anio']
        db_table = 'titulos_cohorte_anexo_seguimiento'
        unique_together = ('cohorte_anexo', 'anio') # -> no funciona, valido a mano

    def __unicode__(self):
        return str(self.anio)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteAnexoSeguimiento, self).__init__(*args, **kwargs)
