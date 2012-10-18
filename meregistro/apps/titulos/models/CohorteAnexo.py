# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Anexo import Anexo
from apps.titulos.models.Cohorte import Cohorte
from apps.titulos.models.EstadoCohorteAnexo import EstadoCohorteAnexo
import datetime

"Cada asignación de una cohorte a un anexo"
class CohorteAnexo(models.Model):
    anexo = models.ForeignKey(Anexo, related_name='cohortes')
    cohorte = models.ForeignKey(Cohorte)
    oferta = models.NullBooleanField()
    emite = models.NullBooleanField()
    estado = models.ForeignKey(EstadoCohorteAnexo) # Concuerda con el último estado en CohorteEstablecimientoEstado

    class Meta:
        app_label = 'titulos'
        ordering = ['cohorte__anio']
        db_table = 'titulos_cohortes_anexos'
        unique_together = ('anexo', 'cohorte')

    def __unicode__(self):
        return str(self.anexo) + ' - ' + str(self.cohorte)

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(CohorteAnexo, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()

    "La cohorte fue aceptada por el anexo?"
    def aceptada(self):
        return self.estado.nombre == EstadoCohorteAnexo.ACEPTADA

    def registrar_estado(self):
        from apps.titulos.models.CohorteAnexoEstado import CohorteAnexoEstado
        registro = CohorteAnexoEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.cohorte_anexo_id = self.id
        registro.save()

    def getEstados(self):
        from apps.titulos.models.CohorteAnexoEstado import CohorteAnexoEstado
        try:
            estados = CohorteAnexoEstado.objects.filter(cohorte_anexo = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

