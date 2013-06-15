# -*- coding: utf-8 -*-

from apps.registro.models import Anexo, Establecimiento, ExtensionAulica
from apps.validez_nacional.models import EstadoSolicitud, Solicitud, SolicitudAnexo, \
    SolicitudEstablecimiento, ValidezNacional
from apps.titulos.models import TituloNacional, NormativaNacional, Carrera, \
    EstadoTituloNacional, Carrera, EstadoCarrera, EstadoNormativaNacional, \
    NormativaJurisdiccional, EstadoNormativaJurisdiccional, TipoNormativaJurisdiccional, \
    NormativaMotivoOtorgamiento
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

FIELD_SEPARATOR = '$'


class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Migra validez'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        filename = args[0]
        fp = open(filename)
        i = 1
        for line in fp:
            registro = self.parsear_linea(line)
            try:
                self.migrar(registro, i)
            except Exception as e:
                print e
                raise CommandError("Error procesando registro nro:" + str(i)
                + "\n")
            i += 1
        fp.close()

    def parsear_linea(self, linea):
        fields = map(lambda x: x.strip(), linea.split(FIELD_SEPARATOR))
        return {
            'jurisdiccion': fields[0],
            'cue': fields[1],
            'nombre_ue': fields[2],
            'titulo': fields[3],
            'carrera': fields[4],
            'primera': fields[5],
            'ultima': fields[6],
            'normativa_jurisdiccional': fields[7],
            'normativa_nacional': fields[8],
            'nroinfd': fields[9]
               }

    def migrar(self, registro, reg_num):
        ue = self.find_unidad_educativa(registro['cue'])
        if ue is None:
            print "UE no encontrada ", registro['cue']
            return
        jurisdiccion = self.get_ue_jurisdiccion(ue)
        carrera = self.find_carrera_nacional(registro['carrera'], jurisdiccion)
        titulo_nacional = self.find_titulo_nacional(registro['titulo'], registro['normativa_nacional'], carrera)
        #estado = EstadoSolicitud.objects.get(nombre=EstadoSolicitud.CONTROLADO)
        solicitud = self.find_solicitud(jurisdiccion, titulo_nacional, carrera,
            registro['primera'], registro['ultima'], registro['normativa_nacional'])
        for norm in registro['normativa_jurisdiccional'].split(';'):
            norm = norm.strip()
            normativa_jurisdiccional = self.find_normativa_jurisdiccional(jurisdiccion, norm)
            self.asociar_solicitud_normativa_jurisdiccional(solicitud, normativa_jurisdiccional)
        self.asociar_solicitud_ue(solicitud, ue)
        self.crear_validez(solicitud, ue, registro['nroinfd'])
        
    def find_unidad_educativa(self, cue):
        for cls in [Anexo, Establecimiento, ExtensionAulica]:
            q = cls.objects.filter(cue=cue)
            if len(q) > 0:
                return q[0]
        return None
        raise Exception("Unidad Educativa no encontrada cue:" + str(cue))


    def get_ue_jurisdiccion(self, ue):
        if ue.__class__ is Establecimiento:
            return ue.dependencia_funcional.jurisdiccion
        elif ue.__class__ is Anexo:
            return ue.establecimiento.dependencia_funcional.jurisdiccion
        elif ue.__class__ is ExtensionAulica:
            return ue.establecimiento.dependencia_funcional.jurisdiccion
        raise Exception("Clase de UE invalida")


    def find_titulo_nacional(self, nombre, normativa, carrera):
        q = TituloNacional.objects.filter(nombre=nombre, normativa_nacional__numero=normativa)
        if len(q) > 0:
            q[0].carreras.add(carrera)
            q[0].save()
            return q[0]
        titulo = TituloNacional()
        titulo.nombre = nombre
        titulo.normativa_nacional = self.find_normativa_nacional(normativa)
        titulo.estado = EstadoTituloNacional.objects.get(nombre=EstadoTituloNacional.VIGENTE)
        titulo.save()
        titulo.registrar_estado()
        try:
            titulo.carreras.add(carrera)
        except: pass
        titulo.save()
        return titulo


    def find_carrera_nacional(self, nombre, jurisdiccion):
        q = Carrera.objects.filter(nombre=nombre)
        if len(q) > 0:
            q[0].jurisdicciones.add(jurisdiccion)
            q[0].save()
            return q[0]
        carrera = Carrera()
        carrera.nombre = nombre
        carrera.estado = EstadoCarrera.objects.get(nombre=EstadoCarrera.VIGENTE)
        carrera.save()
        carrera.registrar_estado()
        carrera.jurisdicciones.add(jurisdiccion)
        carrera.save()
        return carrera

    def find_normativa_nacional(self, numero):
        q = NormativaNacional.objects.filter(numero=numero)
        if len(q) > 0:
            return q[0]
        normativa = NormativaNacional()
        normativa.numero = numero
        normativa.estado = EstadoNormativaNacional.objects.get(nombre=EstadoNormativaNacional.VIGENTE)
        normativa.save()
        normativa.registrar_estado()
        return normativa


    def find_solicitud(self, jurisdiccion, titulo_nacional, carrera, primera,
        ultima, normativa_nacional):
        q = Solicitud.objects.filter(jurisdiccion=jurisdiccion, 
            titulo_nacional=titulo_nacional, carrera=carrera,
            primera_cohorte=primera, ultima_cohorte=ultima,
            normativas_nacionales=normativa_nacional)
        if len(q) > 0:
            return q[0]
        solicitud = Solicitud()
        solicitud.jurisdiccion = jurisdiccion
        solicitud.titulo_nacional = titulo_nacional
        solicitud.carrera = carrera
        solicitud.primera_cohorte = primera
        solicitud.ultima_cohorte = ultima
        solicitud.normativas_nacionales = normativa_nacional
        solicitud.estado = EstadoSolicitud.objects.get(nombre=EstadoSolicitud.CONTROLADO)
        solicitud.save()
        solicitud.registrar_estado()
        return solicitud

    def find_normativa_jurisdiccional(self, jurisdiccion, numero):
        q = NormativaJurisdiccional.objects.filter(jurisdiccion=jurisdiccion, numero_anio=numero)
        if len(q) > 0:
            return q[0]
        normativa = NormativaJurisdiccional()
        normativa.numero_anio = numero
        normativa.jurisdiccion = jurisdiccion
        normativa.estado = EstadoNormativaJurisdiccional.objects.get(nombre=EstadoNormativaJurisdiccional.VIGENTE)
        normativa.tipo_normativa_jurisdiccional = TipoNormativaJurisdiccional.objects.get(nombre="Resolución")
        normativa.otorgada_por = NormativaMotivoOtorgamiento.objects.get(nombre="Aprobación/Implementación") 
        normativa.save()
        normativa.registrar_estado()
        return normativa

    def asociar_solicitud_normativa_jurisdiccional(self, solicitud, normativa_jurisdiccional):
        solicitud.normativas_jurisdiccionales.add(normativa_jurisdiccional)
        solicitud.save()

    def asociar_solicitud_ue(self, solicitud, ue):
        if ue.__class__ is Establecimiento:
            q = SolicitudEstablecimiento.objects.filter(establecimiento=ue, solicitud=solicitud)
            if len(q) == 0:
                asoc = SolicitudEstablecimiento()
                asoc.solicitud = solicitud
                asoc.establecimiento = ue
                asoc.save()
        elif ue.__class__ is Anexo:
            q = SolicitudAnexo.objects.filter(anexo=ue, solicitud=solicitud)
            if len(q) == 0:
                asoc = SolicitudAnexo()
                asoc.solicitud = solicitud
                asoc.anexo = ue
                asoc.save()
        else:
            raise Exception("tipo de ue invalido")


    def crear_validez(self, solicitud, ue, nroinfd):
        if len(ValidezNacional.objects.filter(cue=ue.cue, solicitud=solicitud, nro_infd=nroinfd)) > 0:
            return
        v = ValidezNacional()
        v.solicitud = solicitud
        v.nro_infd = nroinfd
        v.cue = ue.cue
        v.unidad_educativa_id = ue.id
        if ue.__class__ is Establecimiento:
            v.tipo_unidad_educativa = ValidezNacional.TIPO_UE_SEDE
        else:
            v.tipo_unidad_educativa = ValidezNacional.TIPO_UE_ANEXO
        v.save()
        return v
