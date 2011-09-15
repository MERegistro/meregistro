# -*- coding: utf-8 -*-
from django.db import models
from apps.titulos.models.EgresadosAnexo import EgresadosAnexo


class EgresadosAnexoDetalle(models.Model):
    egresados_anexo = models.ForeignKey(EgresadosAnexo, related_name = 'detalle')
    anio_ingreso = models.PositiveIntegerField()
    cantidad_egresados = models.PositiveIntegerField()

    class Meta:
        app_label = 'titulos'
        ordering = ['anio_ingreso']
        db_table = 'titulos_egresados_anexo_detalle'
        unique_together = ('egresados_anexo', 'anio_ingreso')

    def __unicode__(self):
        return str(self.anio_ingreso) + ': '+ str(self.cantidad_egresados)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(EgresadosAnexoDetalle, self).__init__(*args, **kwargs)
