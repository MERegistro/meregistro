# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models import Jurisdiccion
from apps.titulos.models import Carrera, TituloNacional, EstadoTituloNacional, NormativaJurisdiccional
from apps.validez_nacional.models import EstadoSolicitud
import datetime

"""
Solicitud de validez de Título nacional
"""
class Solicitud(models.Model):
    jurisdiccion = models.ForeignKey(Jurisdiccion, null=False)
    carrera = models.ForeignKey(Carrera, null=False)
    titulo_nacional = models.ForeignKey(TituloNacional, null=False)
    primera_cohorte = models.PositiveIntegerField(null=True)
    ultima_cohorte = models.PositiveIntegerField(null=True)
    dictamen_cofev = models.CharField(max_length=200, null=True)
    normativas_jurisdiccionales = models.ManyToManyField(NormativaJurisdiccional, db_table='validez_nacional_solicitud_normativas_jurisdiccionales')
    normativas_nacionales = models.CharField(max_length=99, null=True)
    estado = models.ForeignKey(EstadoSolicitud, null=False) # Concuerda con el último estado en SolicitudEstado
	
    class Meta:
        app_label = 'validez_nacional'

    def __unicode__(self):
        return self.titulo.nombre

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Solicitud, self).__init__(*args, **kwargs)
        self.estados = self.get_estados()

    "Sobreescribo para eliminar los objetos relacionados"
    def delete(self, *args, **kwargs):
        for normativa in self.normativas.all():
            normativa.delete()
        for est in self.estados.all():
            est.delete()
        super(Solicitud, self).delete(*args, **kwargs)

    def registrar_estado(self):
        from apps.validez_nacional.models import SolicitudEstado
        registro = SolicitudEstado(estado=self.estado)
        registro.fecha = datetime.date.today()
        registro.solicitud_id = self.id
        registro.save()

    def get_estados(self):
        from apps.validez_nacional.models import SolicitudEstado
        try:
            estados = SolicitudEstado.objects.filter(solicitud=self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def get_cues(self):
        return {}
