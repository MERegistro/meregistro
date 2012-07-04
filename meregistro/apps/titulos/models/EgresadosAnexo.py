# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.titulos.models.TituloJurisdiccional import TituloJurisdiccional
import datetime


class EgresadosAnexo(models.Model):

    ANIO_MAXIMO_EGRESADOS = 2008
    
    anexo = models.ForeignKey(Anexo, related_name = 'egresados')
    titulo_jurisdiccional = models.ForeignKey(TituloJurisdiccional)
    anio = models.PositiveIntegerField()
    cantidad_egresados = models.PositiveIntegerField()
    revisado_jurisdiccion = models.NullBooleanField(default = False, null = True)

    class Meta:
        app_label = 'titulos'
        ordering = ['anio']
        db_table = 'titulos_egresados_anexo'
        unique_together = ('anexo', 'anio', 'titulo_jurisdiccional')

    def __unicode__(self):
        return str(self.anio) + ': '+ str(self.cantidad_egresados)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(EgresadosAnexo, self).__init__(*args, **kwargs)

    def get_suma_egresados_detalle(self):
        detalle = self.detalle.all()
        if not detalle:
            return None
        return sum([e.cantidad_egresados for e in detalle])
