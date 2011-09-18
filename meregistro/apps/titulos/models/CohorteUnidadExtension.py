# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.UnidadExtension import UnidadExtension
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteUnidadExtension import EstadoCohorteUnidadExtension
import datetime

"Cada asignación de una cohorte a un anexo"
class CohorteUnidadExtension(models.Model):
    unidad_extension = models.ForeignKey(UnidadExtension, related_name = 'unidad_extension_cohortes')
    cohorte = models.ForeignKey(Cohorte)
    oferta = models.NullBooleanField()
    inscriptos = models.PositiveIntegerField(null = True, blank = True)
    estado = models.ForeignKey(EstadoCohorteUnidadExtension) # Concuerda con el último estado en CohorteUnidadExtensionEstado

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte__anio']
        db_table = 'titulos_cohortes_unidades_extension'
        unique_together = ('unidad_extension', 'cohorte')

    def __unicode__(self):
        return str(self.unidad_extension) + ' - ' + str(self.cohorte)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteUnidadExtension, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    "La cohorte fue aceptada por el anexo?"
    def aceptada(self):
        return self.estado.nombre == EstadoCohorteUnidadExtension.ACEPTADA

    def registrar_estado(self):
        from apps.titulos.models.CohorteUnidadExtensionEstado import CohorteUnidadExtensionEstado
        registro = CohorteUnidadExtensionEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.cohorte_unidad_extension_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.CohorteUnidadExtensionEstado import CohorteUnidadExtensionEstado
        try:
            estados = CohorteUnidadExtensionEstado.objects.filter(cohorte_unidad_extension = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados
