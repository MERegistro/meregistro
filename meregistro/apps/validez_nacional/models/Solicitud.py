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
    nro_expediente = models.CharField(max_length=200, null=True)
    nro_expediente_gedo = models.CharField(max_length=200, null=True)
    normativas_jurisdiccionales = models.ManyToManyField(NormativaJurisdiccional, db_table='validez_nacional_solicitud_normativas_jurisdiccionales')
    normativas_nacionales = models.CharField(max_length=99, null=True)
    estado = models.ForeignKey(EstadoSolicitud, null=False) # Concuerda con el último estado en SolicitudEstado
    normativa_jurisdiccional_migrada = models.CharField(max_length=99, null=True)
    
    class Meta:
        app_label = 'validez_nacional'

    def __unicode__(self):
        return self.titulo_nacional.nombre

    def get_nro_expediente_completo(self):
        if self.nro_expediente != None:
            return self.nro_expediente
        elif self.nro_expediente_gedo != None:
            return 'EX-' + self.nro_expediente_gedo + '- -APN-DVNTYE#ME'
            return 3
        else:
            return ''

    "Sobreescribo el init para agregarle propiedades"
    def __init__(self, *args, **kwargs):
        super(Solicitud, self).__init__(*args, **kwargs)
        self.estados = self.get_estados()

    "Sobreescribo para eliminar los objetos relacionados"
    def delete(self, *args, **kwargs):
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

    """
    Asocia/elimina los establecimientos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_establecimientos(self, establecimientos_procesados_ids, current_establecimientos_ids, establecimientos_seleccionados_ids):
        from apps.validez_nacional.models import SolicitudEstablecimiento
        
        "Borrar los que se des-chequean"
        for est_id in establecimientos_procesados_ids:
            if (str(est_id) not in establecimientos_seleccionados_ids) \
                and (est_id in current_establecimientos_ids): 
                # Si no está en los ids de la página, borrarlo
                SolicitudEstablecimiento.objects.get(solicitud__id=self.id, establecimiento=est_id).delete()

        "Agregar los nuevos"
        for est_id in establecimientos_seleccionados_ids:
            if int(est_id) not in current_establecimientos_ids:
                # Lo creo y registro el estado
                registro = SolicitudEstablecimiento.objects.create(solicitud=self, establecimiento_id=est_id)


    """
    Asocia/elimina los establecimientos desde el formulario masivo
    XXX: los valores "posts" vienen como strings
    """
    def save_anexos(self, anexos_procesados_ids, current_anexos_ids, anexos_seleccionados_ids):
        
        from apps.validez_nacional.models import SolicitudAnexo
        
        "Borrar los que se des-chequean"
        for est_id in anexos_procesados_ids:
            if (str(est_id) not in anexos_seleccionados_ids) and (est_id in current_anexos_ids): # Si no está en los ids de la página, borrarlo
                SolicitudAnexo.objects.get(solicitud__id=self.id, anexo=est_id).delete()

        "Agregar los nuevos"
        for est_id in anexos_seleccionados_ids:
            if int(est_id) not in current_anexos_ids:
                # Lo creo y registro el estado
                registro = SolicitudAnexo.objects.create(solicitud=self, anexo_id=est_id)


    def is_deletable(self):
        return self.estado.nombre in EstadoSolicitud.PENDIENTE
        

    def is_numerable(self):
        numerable = self.estado.nombre in [EstadoSolicitud.EVALUADO, EstadoSolicitud.CONTROLADO] 
        numerable = numerable and (len(self.establecimientos.all()) > 0 or len(self.anexos.all()) > 0)
        numerable = numerable and self.jurisdiccion and self.carrera and self.primera_cohorte and self.ultima_cohorte \
            and (self.normativas_jurisdiccionales or self.normativa_jurisdiccional_migrada) and self.normativas_nacionales
        return numerable


    def numerado(self):
        return self.estado.nombre == EstadoSolicitud.NUMERADO


    def tiene_unidades_asignadas(self):
        return (self.establecimientos.count() + self.anexos.count()) > 0


    def generar_informe(self):
        from apps.validez_nacional.models import InformeSolicitud
        informe = InformeSolicitud()
        informe.solicitud_id = self.id
        informe.save()

        return informe
