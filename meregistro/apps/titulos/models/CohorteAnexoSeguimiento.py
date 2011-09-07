# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.CohorteAnexo import CohorteAnexo
import datetime

"Seguimiento de cada cohorte del anexo"
class CohorteAnexoSeguimiento(models.Model):
    cohorte_anexo = models.ForeignKey(CohorteAnexo, editable = False, related_name = 'seguimiento')
    anio = models.PositiveIntegerField()
    solo_cursan_nueva = models.PositiveIntegerField(null = True, blank = True)
    solo_recursan = models.PositiveIntegerField(null = True, blank = True)
    recursan_cursan = models.PositiveIntegerField(null = True, blank = True)
    no_cursan = models.PositiveIntegerField(null = True, blank = True)
    observaciones = models.CharField(max_length = 255, null = True, blank = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte_establecimiento__cohorte__anio']
        db_table = 'titulos_cohorte_anexo_seguimiento'

    def __unicode__(self):
        return str(self.cohorte_anexo.cohorte.anio)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteAnexoSeguimiento, self).__init__(*args, **kwargs)
