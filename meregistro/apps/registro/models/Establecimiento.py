# -*- coding: utf-8 -*-
from django.db import models
from apps.registro.models.TipoNormativa import TipoNormativa
from apps.registro.models.Jurisdiccion import Jurisdiccion
from apps.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from apps.registro.models.DependenciaFuncional import DependenciaFuncional
from apps.registro.models.Alcance import Alcance
from apps.registro.models.Funcion import Funcion
from apps.registro.models.Turno import Turno
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.TipoNorma import TipoNorma
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from apps.seguridad.models import Ambito
import datetime
from apps.seguridad.audit import audit
from apps.registro.models.TipoSubsidio import TipoSubsidio
from apps.seguridad.models.TipoDocumento import TipoDocumento

@audit
class Establecimiento(models.Model):
    YEARS_CHOICES = [(int(n), int(n)) for n in range(1800,2021)]
    CODIGO_TIPO_UNIDAD_EDUCATIVA = '00'  # Para completar el CUE

    dependencia_funcional = models.ForeignKey(DependenciaFuncional)
    cue = models.CharField(max_length=9, unique=True)
    nombre = models.CharField(max_length=255)
    unidad_academica = models.BooleanField()
    nombre_unidad_academica = models.CharField(max_length=100, null=True, blank=True)
    subsidio = models.ForeignKey(TipoSubsidio)
    tipo_normativa = models.ForeignKey(TipoNormativa)
    norma_creacion = models.CharField(max_length=100)
    tipo_norma = models.ForeignKey(TipoNorma, null=False)
    tipo_norma_otra = models.CharField(max_length=100, null=True, blank=True)
    observaciones = models.TextField(max_length=255, null=True, blank=True)
    anio_creacion = models.IntegerField(null=True, blank=True, choices=YEARS_CHOICES)
    telefono = models.CharField(max_length=100, null=True, blank=True)
    interno = models.CharField(max_length=10, null=True, blank=True)
    fax = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    sitio_web = models.URLField(max_length=255, null=True, blank=True, verify_exists=False)
    solicitud_filename = models.CharField(max_length=100, null=True, blank=True, editable=False)
    ambito = models.ForeignKey(Ambito, editable=False, null=True)
    #turnos = models.ManyToManyField(Turno, blank=True, null=True, db_table='registro_establecimientos_turnos')
    turnos = models.ManyToManyField(Turno, blank=True, null=True, through='EstablecimientoTurno')
    alcances = models.ManyToManyField(Alcance, blank=True, null=True, db_table='registro_establecimientos_alcances')
    funciones = models.ManyToManyField(Funcion, blank=True, null=True, db_table='registro_establecimientos_funciones')
    estado = models.ForeignKey(EstadoEstablecimiento, editable=False, null=True)
    posee_centro_estudiantes = models.NullBooleanField(null=True)
    posee_representantes_estudiantiles = models.NullBooleanField(null=True)
    # Fusión con autoridades
    director_apellido = models.CharField(max_length=40, null=False)
    director_nombre = models.CharField(max_length=40, null=False)
    director_fecha_nacimiento = models.DateField(null=True)
    director_tipo_documento = models.ForeignKey(TipoDocumento, null=True, blank=True)
    director_documento = models.CharField(max_length=20, null=True, blank=True)
    director_telefono = models.CharField(max_length=30, null=True, blank=True)
    director_celular = models.CharField(max_length=30, null=True, blank=True)
    director_email = models.EmailField(max_length=255, null=True, blank=True)
    
    class Meta:
        app_label = 'registro'
        ordering = ['nombre']

    """
    Sobreescribo el init para agregarle propiedades
    """
    def __init__(self, *args, **kwargs):
        super(Establecimiento, self).__init__(*args, **kwargs)
        self.registro_estados = RegistroEstablecimiento.objects.filter(establecimiento=self).order_by('id')
        self.estado_actual = self.getEstadoActual()
        from apps.registro.models import CERTIFICACION_CARGA_ANIOS_HABILITADOS
        self.carga_certificada_anio_actual = self.carga_certificada(CERTIFICACION_CARGA_ANIOS_HABILITADOS[-1])


    def __unicode__(self):
        return str(self.cue) + ' - ' + self.nombre


    def clean(self):
        # Chequea que la combinación entre jurisdiccion y cue sea única
        try:
            est = Establecimiento.objects.get(cue=self.cue, dependencia_funcional__jurisdiccion__id=self.dependencia_funcional.jurisdiccion.id)
            if est and est != self:
                raise ValidationError('Los datos ingresados corresponden a una Sede que ya se encuentra registrada.')
        except ObjectDoesNotExist:
            pass


    def registrar_estado(self, estado, observaciones=''):
        registro = RegistroEstablecimiento(estado=estado)
        registro.fecha = datetime.date.today()
        registro.establecimiento_id = self.id
        registro.observaciones = observaciones
        self.estado = estado
        registro.save()
        self.save()


    def save(self):
        self.updateAmbito()
        if self.id is not None:
            self.ambito.vigente = (self.estado.nombre != EstadoEstablecimiento.PENDIENTE)
        self.ambito.save()
        models.Model.save(self)


    def delete(self):
        if self.getEstadoActual() == EstadoEstablecimiento.PENDIENTE:
            RegistroEstablecimiento.objects.filter(establecimiento=self).delete()
            models.Model.delete(self)
            if self.ambito is not None:
              try:
                self.ambito.delete()
              except:
                pass
        else:
            estado = EstadoEstablecimiento.objects.get(nombre=EstadoEstablecimiento.NO_VIGENTE)
            self.registrar_estado(estado)


    def updateAmbito(self):
        if self.pk is None or self.ambito is None:
            try:
                self.ambito = self.dependencia_funcional.ambito.createChild(self.cue + ' - ' + self.nombre, self)
            except Exception:
                pass
        else:
            self.ambito.set_parent(self.dependencia_funcional.ambito)
            self.ambito.descripcion = self.cue + ' - ' + self.nombre
            self.ambito.save()


    def hasAnexos(self):
        from apps.registro.models.Anexo import Anexo
        anexos = Anexo.objects.filter(establecimiento=self)
        return anexos.count() > 0


    def getEstadoActual(self):
        estado_actual = self.estadoActual()
        if estado_actual is None:
            return u''
        return str(estado_actual)


    def estadoActual(self):
        try:
            return list(self.registro_estados)[-1].estado
        except IndexError:
            return None


    """
    Se puede eliminar cuando:
     * Tiene un sólo estado y es pendiente
     (hoy día si tiene un sólo estado ES pendiente)
    """
    def isDeletable(self):
        cant_estados = len(self.registro_estados) is 1
        es_pendiente = self.estado_actual == u'Pendiente'
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


    """
    Obtener las partes del cue desde la clase, dando el cue como parámetro
    """
    @classmethod
    def get_parts_from_cue(cls, cue):
        try:
            tmp = int(cue)
        except ValueError:  # Tiene más que números
            return None
        if len(cue) != 9:  # CUE inválido
            return None
        parts = {
            'codigo_jurisdiccion': cue[0:2],
            'cue': cue[2:7],
            'codigo_tipo_unidad_educativa': cue[7:9],
        }
        return parts


    def get_first_domicilio(self):
        try:
            dom = self.domicilios.all()[0]
        except IndexError:
            return None
        return dom

    
    def get_domicilio_institucional(self):
        from apps.registro.models import EstablecimientoDomicilio
        try:
            dom = EstablecimientoDomicilio.objects.get(establecimiento=self, tipo_domicilio__descripcion=u'Institucional')
        except EstablecimientoDomicilio.DoesNotExist:
            return None
        except EstablecimientoDomicilio.MultipleObjectsReturned:
            dom = EstablecimientoDomicilio.objects.filter(establecimiento=self, tipo_domicilio__descripcion=u'Institucional')[0]
        return dom


    def get_fecha_solicitud(self):
        try:
            fecha = self.registro_estados.all()[0].fecha.strftime("%d/%m/%Y")
        except IndexError:
            return "---"
        return fecha


    def registrado(self):
        return self.estado.nombre == EstadoEstablecimiento.REGISTRADO


    def pendiente(self):
        return self.estado.nombre == EstadoEstablecimiento.PENDIENTE


    def get_verificacion_datos(self):
        from EstablecimientoVerificacionDatos import EstablecimientoVerificacionDatos
        try:
            verificacion = EstablecimientoVerificacionDatos.objects.get(establecimiento=self)
        except EstablecimientoVerificacionDatos.DoesNotExist:
            verificacion = EstablecimientoVerificacionDatos()
            verificacion.establecimiento = self
            verificacion.save()
        return verificacion


    def verificado(self):
        return self.get_verificacion_datos().completo()

    """
    Se puede certificar la carga del año cuando:
        * Tiene seguimiento de cohorte cargado en ese año | Tiene inscriptos en la cohorte de ese año
        * Cargó la matrícula de ese año  
        * Cargó datos de democratización
    """
    """
    #494
    Para que se pueda certificar tiene que cumplir con las siguientes condiciones:
        1) En seguimiento de cohorte tiene que
            * haber cargado el seguimiento o inscriptos 2016 o
            * haber rechazado o haber hecho fin de seguimiento (new) (​/titulos/cohorte_seguimiento/1234/establecimiento/)
        2) Haber cargado matrícula 2016 de la institución (/​registro/establecimiento/1234/matricula)
    """
    def puede_certificar_carga(self, anio):
        """
        from apps.titulos.models import CohorteEstablecimientoSeguimiento
        from apps.titulos.models import CohorteEstablecimiento
        from apps.registro.models import EstablecimientoMatricula
        seguimiento_cargado = len(CohorteEstablecimientoSeguimiento.objects.filter(cohorte_establecimiento__establecimiento__id=self.id, anio=anio)) > 0
        inscriptos_cargados = len(CohorteEstablecimiento.objects.filter(establecimiento__id=self.id, cohorte__anio=anio, inscriptos__gt=0)) > 0
        matricula_cargada = len(EstablecimientoMatricula.objects.filter(establecimiento__id=self.id, anio=anio)) > 0
        datos_democratizacion_cargados = self.posee_centro_estudiantes is not None and self.posee_representantes_estudiantiles is not None

        return (seguimiento_cargado or inscriptos_cargados) and matricula_cargada and datos_democratizacion_cargados
        """
        # Matricula
        matricula_cargada = self.establecimientomatricula_set.filter(anio=anio).exists()
        if not matricula_cargada:
            return False
        
        # Seguimiento
        """
        Si alguna cohorte no tiene seguimiento de dicho año y no está rechazada o finalizada, no se puede certificar la carga
        NOTA: es lo mismo decir que no está registrada, porque las Asignadas supongo que no cuentan
        """
        from apps.titulos.models import CohorteEstablecimiento, EstadoCohorteEstablecimiento
        cohortes_con_seguimiento_anio = [ce.id for ce in CohorteEstablecimiento.objects.filter(establecimiento__id=self.id, seguimiento__anio=anio)]
        cohortes_anio_con_inscriptos = [ce.id for ce in CohorteEstablecimiento.objects.filter(establecimiento__id=self.id, cohorte__anio=anio, inscriptos__gt=0, estado__nombre=EstadoCohorteEstablecimiento.REGISTRADA)]
        cohortes_sin_seguimiento_anio = CohorteEstablecimiento.objects.filter(establecimiento__id=self.id).exclude(id__in=cohortes_con_seguimiento_anio + cohortes_anio_con_inscriptos)
        for ce in cohortes_sin_seguimiento_anio:
            #if ce.estado.nombre not in [EstadoCohorteEstablecimiento.RECHAZADA, EstadoCohorteEstablecimiento.FINALIZADA, EstadoCohorteEstablecimiento.ASIGNADA]:
            if ce.estado.nombre in [EstadoCohorteEstablecimiento.REGISTRADA]:
                return False
        
        return True


    """
    """
    def certificar_carga(self, anio, usuario):
        from apps.registro.models import EstablecimientoCertificacionCarga
        certificacion = EstablecimientoCertificacionCarga()
        certificacion.anio = anio
        certificacion.usuario_id = usuario.id
        certificacion.establecimiento_id = self.id
        certificacion.fecha = datetime.date.today()
        certificacion.save()
        
        return certificacion

    """
    """
    def carga_certificada(self, anio):
        from apps.registro.models import EstablecimientoCertificacionCarga
        return EstablecimientoCertificacionCarga.objects.filter(establecimiento__id=self.id, anio=anio).exists()
