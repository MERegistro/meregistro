# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteEstablecimiento import EstadoCohorteEstablecimiento
import datetime

"Cada asignación de una cohorte a un establecimiento"
class CohorteEstablecimiento(models.Model):
    establecimiento = models.ForeignKey(Establecimiento, related_name = 'cohortes')
    cohorte = models.ForeignKey(Cohorte)
    oferta = models.NullBooleanField()
    emite = models.NullBooleanField()
    inscriptos = models.PositiveIntegerField(null = True, blank = True)
    estado = models.ForeignKey(EstadoCohorteEstablecimiento) # Concuerda con el último estado en CohorteEstablecimientoEstado

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte__anio']
        db_table = 'titulos_cohortes_establecimientos'
        unique_together = ('establecimiento', 'cohorte')

    def __unicode__(self):
        return str(self.establecimiento) + ' - ' + str(self.cohorte)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteEstablecimiento, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.aceptada = self.aceptada()

    "La cohorte fue aceptada por el establecimiento?"
    def aceptada(self):
        return self.estado.nombre == EstadoCohorteEstablecimiento.ACEPTADA

    def registrar_estado(self):
        from apps.titulos.models.CohorteEstablecimientoEstado import CohorteEstablecimientoEstado
        registro = CohorteEstablecimientoEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.cohorte_establecimiento_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.CohorteEstablecimientoEstado import CohorteEstablecimientoEstado
        try:
            estados = CohorteEstablecimientoEstado.objects.filter(cohorte_establecimiento = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados
