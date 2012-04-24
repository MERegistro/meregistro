# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.TipoNorma import TipoNorma
from apps.registro.models.TipoNormativa import TipoNormativa
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.models.Turno import Turno
from apps.registro.models.Alcance import Alcance
from apps.registro.models.Funcion import Funcion
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from apps.seguridad.models import Ambito
import datetime
from apps.seguridad.audit import audit



@audit
class Anexo(models.Model):
    YEARS_CHOICES = [(int(n), int(n)) for n in range(1800,2021)]
    
    establecimiento = models.ForeignKey(Establecimiento)
    cue = models.CharField(max_length=9, unique=True)
    fecha_alta = models.DateField(null=True, blank=True, editable=False)
    nombre = models.CharField(max_length=255)
    anio_creacion = models.IntegerField(null=True, blank=True, choices=YEARS_CHOICES)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    norma_creacion = models.CharField(max_length=100)
    tipo_norma = models.ForeignKey(TipoNorma, null=False)
    tipo_norma_otra = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    interno = models.CharField(max_length=10, null=True, blank=True)
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    observaciones = models.TextField(max_length=255, null=True, blank=True)
    sitio_web = models.URLField(max_length=255, null=True, blank=True, verify_exists=False)
    #turnos = models.ManyToManyField(Turno, null=True, db_table='registro_anexos_turnos')
    estado = models.ForeignKey(EstadoAnexo) # Concuerda con el último estado en AnexoEstado
    ambito = models.ForeignKey(Ambito, editable=False, null=True)
    alcances = models.ManyToManyField(Alcance, blank=True, null=True, db_table='registro_anexos_alcances')
    funciones = models.ManyToManyField(Funcion, blank=True, null=True, db_table='registro_anexos_funciones')

    class Meta:
        app_label = 'registro'

    def __unicode__(self):
        return self.nombre

    " Sobreescribo el init para agregarle propiedades "
    def __init__(self, *args, **kwargs):
        super(Anexo, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.estado_actual = self.getEstadoActual()


    def clean(self):
        from apps.registro.models.ExtensionAulica import ExtensionAulica  # Lo importo acá para evitar el import loop
        " Chequea que el cue sea único "
        cue = self.cue
        if cue != '':
            try:
                anexo = Anexo.objects.get(cue=cue)
                if anexo and anexo != self:
                    raise ValidationError('Los datos ingresados corresponden a una Unidad Educativa (Anexo) que ya se encuentra registrada')
            except Anexo.DoesNotExist:
                pass
            try:
                ext = ExtensionAulica.objects.get(cue=cue)
                if ext:
                    raise ValidationError('Los datos ingresados corresponden a una Unidad Educativa (Extensión áulica) que ya se encuentra registrada')
            except ExtensionAulica.DoesNotExist:
                pass


    def registrar_estado(self):
        from apps.registro.models.AnexoEstado import AnexoEstado
        registro = AnexoEstado(estado=self.estado)
        registro.fecha = datetime.date.today()
        registro.anexo_id = self.id
        registro.save()

    def getEstados(self):
        from apps.registro.models.AnexoEstado import AnexoEstado
        try:
            estados = AnexoEstado.objects.filter(anexo=self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        if self.id is not None:
            return self.estado
        else:
            return None

    def dadoDeBaja(self):
        return self.estado.nombre == EstadoAnexo.BAJA

    def save(self):
        self.updateAmbito()
        self.ambito.vigente = True
        self.ambito.save()
        models.Model.save(self)

    def updateAmbito(self):
        if self.pk is None or self.ambito is None:
            try:
                self.ambito = self.establecimiento.ambito.createChild(self.nombre, self)
            except Exception:
                pass
        else:
            self.ambito.descripcion = self.nombre
            self.ambito.save()

    def get_first_domicilio(self):
        try:
            dom = self.anexo_domicilio.all()[0]
        except IndexError:
            return None
        return dom

    def is_editable(self):
        es_pendiente = self.estado_actual.nombre == u'Pendiente'
        return es_pendiente

    def is_deletable(self):
        cant_estados = len(self.estados.all()) is 1
        es_pendiente = self.estado_actual.nombre == u'Pendiente'
        return cant_estados == 1 and es_pendiente

    """
    Obtener las partes del cue desde una instancia
    """
    def get_cue_parts(self):
        parts = {
            'codigo_jurisdiccion': self.cue[0:2],
            'cue': self.cue[2:7],
            'codigo_tipo_unidad_educativa': self.cue[7:9],
        }
        return parts
        
    def get_fecha_solicitud(self):
        try:
            fecha = self.estados.all()[0].fecha.strftime("%d/%m/%Y")
        except IndexError:
            return "---"
        return fecha

    def registrado(self):
        return self.estado.nombre == EstadoAnexo.REGISTRADO

    def pendiente(self):
        return self.estado.nombre == EstadoAnexo.PENDIENTE

    def get_verificacion_datos(self):
        from AnexoVerificacionDatos import AnexoVerificacionDatos
        try:
            verificacion = AnexoVerificacionDatos.objects.get(anexo=self)
        except AnexoVerificacionDatos.DoesNotExist:
            verificacion = AnexoVerificacionDatos()
            verificacion.anexo = self
            verificacion.save()
        return verificacion

    def verificado(self):
        return self.get_verificacion_datos().completo()

    def delete(self):
        models.Model.delete(self)
        if self.is_deletable() and self.ambito is not None:
            try:
                self.ambito.delete()
            except:
                pass
