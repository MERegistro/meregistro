# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Anexo import Anexo
from apps.registro.models.TipoNormativa import TipoNormativa
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.models.Turno import Turno
from apps.registro.models.Alcance import Alcance
from apps.registro.models.Funcion import Funcion
from apps.seguridad.models.Ambito import Ambito
from apps.registro.models.OrigenNorma import OrigenNorma
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import datetime
from apps.seguridad.audit import audit
from apps.registro.models.TipoSubsidio import TipoSubsidio

@audit
class ExtensionAulica(models.Model):
    NORMA_CREACION_CHOICES = ['Decreto', 'Resolución', 'Disposición', 'Dictamen', 'Otra']
    YEARS_CHOICES = [(int(n), str(n)) for n in range(1800, datetime.datetime.now().year + 1)]
    
    establecimiento = models.ForeignKey(Establecimiento)
    cue = models.CharField(max_length=9, null=True, blank=True, unique=True)
    nombre = models.CharField(max_length = 255)
    observaciones = models.CharField(max_length = 255)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    fecha_alta = models.DateField(null=True, blank=True, editable=False)
    normativa = models.CharField(max_length = 100)
    anio_creacion = models.IntegerField(null=True, blank=True, choices = YEARS_CHOICES)
    norma_creacion = models.CharField(max_length=100)
    norma_creacion_otra = models.CharField(max_length=100)
    norma_creacion_numero = models.CharField(max_length=100)
    sitio_web = models.URLField(max_length = 255, null = True, blank = True, verify_exists = False)
    telefono = models.CharField(max_length = 100, null = True, blank = True)
    email = models.EmailField(max_length = 255, null = True, blank = True)
    #turnos = models.ManyToManyField(Turno, null = True, db_table = 'registro_extensiones_aulicas_turnos')
    estado = models.ForeignKey(EstadoExtensionAulica) # Concuerda con el último estado en ExtensionAulicaEstado
    alcances = models.ManyToManyField(Alcance, blank=True, null=True, db_table='registro_extension_aulica_alcances')
    funciones = models.ManyToManyField(Funcion, blank=True, null=True, db_table='registro_extension_aulica_funciones')
    ambito = models.ForeignKey(Ambito, editable=False, null=True)
    origen_norma = models.ForeignKey(OrigenNorma, null=False)
    subsidio = models.ForeignKey(TipoSubsidio)  # XXX Esto no está implementado en el formulario, por eso falla

    class Meta:
        app_label = 'registro'
        ordering = ['nombre']
        db_table = 'registro_extension_aulica'

    def __init__(self, *args, **kwargs):
        super(ExtensionAulica, self).__init__(*args, **kwargs)
        self.estados = self.getEstados()
        self.estado_actual = self.getEstadoActual()

    def __unicode__(self):
        return self.nombre
        
    def clean(self):
        " Chequea que el cue sea único "
        cue = self.cue
        if cue != '':
            try:
                ext = ExtensionAulica.objects.get(cue=cue)
                if ext and ext != self:
                    raise ValidationError('Los datos ingresados corresponden a una Unidad Educativa (Extensión áulica) que ya se encuentra registrada')
            except ExtensionAulica.DoesNotExist:
                pass
            try:
                anexo = Anexo.objects.get(cue=cue)
                if anexo:
                    raise ValidationError('Los datos ingresados corresponden a una Unidad Educativa (Anexo) que ya se encuentra registrada')
            except Anexo.DoesNotExist:
                pass
                
    def registrar_estado(self):
        from apps.registro.models.ExtensionAulicaEstado import ExtensionAulicaEstado
        registro = ExtensionAulicaEstado(estado = self.estado)
        registro.fecha = datetime.date.today()
        registro.extension_aulica_id = self.id
        registro.save()

    def getEstados(self):
        from apps.registro.models.ExtensionAulicaEstado import ExtensionAulicaEstado
        try:
            estados = ExtensionAulicaEstado.objects.filter(extension_aulica = self).order_by('fecha', 'id')
        except:
            estados = {}
        return estados

    def getEstadoActual(self):
        if self.id is not None:
            return self.estado
        else:
            return None

    def dadaDeBaja(self):
        return self.estado.nombre == EstadoExtensionAulica.BAJA
        
    def is_editable(self):
        es_pendiente = self.estado_actual.nombre == u'Pendiente'
        return es_pendiente

    def is_deletable(self):
        cant_estados = len(self.estados.all()) is 1
        es_pendiente = self.estado_actual.nombre == u'Pendiente'
        return cant_estados == 1 and es_pendiente

    def get_fecha_solicitud(self):
        try:
            fecha = self.estados.all()[0].fecha.strftime("%d/%m/%Y")
        except IndexError:
            return "---"
        return fecha


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


    def registrado(self):
        return self.estado.nombre == EstadoExtensionAulica.REGISTRADA

    def pendiente(self):
        return self.estado.nombre == EstadoExtensionAulica.PENDIENTE


    def get_verificacion_datos(self):
        from ExtensionAulicaVerificacionDatos import ExtensionAulicaVerificacionDatos
        try:
            verificacion = ExtensionAulicaVerificacionDatos.objects.get(extension_aulica=self)
        except ExtensionAulicaVerificacionDatos.DoesNotExist:
            verificacion = ExtensionAulicaVerificacionDatos()
            verificacion.extension_aulica = self
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

    def get_first_domicilio(self):
        try:
            dom = self.domicilio.all()[0]
        except IndexError:
            return None
        return dom