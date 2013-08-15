# -*- coding: utf-8 -*-

from apps.registro.models import Anexo, Establecimiento, ExtensionAulica
from apps.titulos.models import Carrera, EstadoCarrera, CarreraJurisdiccional, \
 CarreraJurisdiccionalCohorte, \
 EstadoCarreraJurisdiccional, Cohorte, CohorteAnexo, CohorteEstablecimiento, \
 CohorteExtensionAulica, EstadoCohorteEstablecimiento, EstadoCohorteAnexo, \
 EstadoCohorteExtensionAulica, \
 CohorteAnexoSeguimiento, CohorteEstablecimientoSeguimiento, CohorteExtensionAulicaSeguimiento
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

FIELD_SEPARATOR = '$'


class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Migra una seguimiento'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        filename = args[0]
        name = filename.split("/")[-1:][0].split(".")[0]
        jur, primera, ultima = name.split("-")
        fp = open(filename)
        i = 1
        for line in fp:
            registro = self.parsear_linea(line)
            registro['primera'] = int(primera)
            registro['ultima'] = int(ultima)
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
            'cue_anexo': fields[2],
            'carrera': fields[4],
            'inscriptos': fields[5],
            'seguimiento': fields[6:]
               }

    def migrar(self, registro, reg_num):
        ue = self.find_unidad_educativa(registro['cue_anexo'])
        if ue is None: return
        jurisdiccion = self.get_ue_jurisdiccion(ue)
        carrera_jurisdiccional, cohorte = self.asociar_carrera_jurisdiccion(registro['carrera'],
			jurisdiccion, registro['primera'])
        #cohorte = self.get_cohorte(carrera_jurisdiccional, registro['primera'])
        cohorte_ue = self.create_cohorte_ue(cohorte, ue, registro['inscriptos'])
        i = 0
        print registro['cue_anexo'], registro['carrera']
        for anio in range(registro['primera']+1, registro['ultima']+1):
            seguimiento_anios = map(lambda x: 0 if x == '' else int(x),
                registro['seguimiento'][i*5:(i+1)*5])
            if sum(seguimiento_anios) > 0:
                self.create_seguimiento(cohorte_ue, anio, seguimiento_anios)
            i += 1
        
        
    def find_unidad_educativa(self, cue):
        for cls in [Anexo, Establecimiento, ExtensionAulica]:
            q = cls.objects.filter(cue=cue)
            if len(q) > 0:
                return q[0]
        print "Unidad Educativa no encontrada cue:" + str(cue)
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


    def asociar_carrera_jurisdiccion(self, carrera_nombre, jurisdiccion, primera):
        q = Carrera.objects.filter(nombre=carrera_nombre)
        if len(q) == 0:
            # crear carrera
            carrera = Carrera()
            carrera.nombre = carrera_nombre
            carrera.estado = EstadoCarrera.objects.get(nombre=EstadoCarrera.VIGENTE)
            carrera.save()
            carrera.registrar_estado()
        else:
            carrera = q[0]
        q = (CarreraJurisdiccional.objects.filter(carrera=carrera)
                .filter(jurisdiccion=jurisdiccion)
                #.filter(datos_cohorte__primera_cohorte_autorizada=primera)
                #.filter(datos_cohorte__ultima_cohorte_autorizada=primera)
            )  
        if len(q) == 0:
            carrera_jurisdiccional = CarreraJurisdiccional()
            carrera_jurisdiccional.carrera = carrera
            carrera_jurisdiccional.jurisdiccion = jurisdiccion
            carrera_jurisdiccional.estado = EstadoCarreraJurisdiccional.objects.get(nombre=EstadoCarreraJurisdiccional.REGISTRADO)
            carrera_jurisdiccional.save()
            carrera_jurisdiccional.registrar_estado() 
            carrera.jurisdicciones.add(jurisdiccion)
            print carrera.id, " ", jurisdiccion.id
        else:
            carrera_jurisdiccional = q[0]
        return carrera_jurisdiccional, self.get_cohorte(carrera_jurisdiccional, int(primera))

    def get_cohorte(self, carrera_jurisdiccional, anio):
        q = (Cohorte.objects.filter(carrera_jurisdiccional=carrera_jurisdiccional)
            .filter(anio=anio))
        if len(q) == 0:
            cohorte = Cohorte()
            cohorte.carrera_jurisdiccional = carrera_jurisdiccional
            cohorte.anio = anio
            cohorte.save()
        else:
            cohorte = q[0]
        carrera_cohorte = CarreraJurisdiccionalCohorte()
        carrera_cohorte.carrera_jurisdiccional = carrera_jurisdiccional
        carrera_cohorte.primera_cohorte_solicitada = 2008
        carrera_cohorte.primera_cohorte_autorizada = 2008
        carrera_cohorte.ultima_cohorte_solicitada = 2050
        carrera_cohorte.ultima_cohorte_autorizada = 2050
        if len(CarreraJurisdiccionalCohorte.objects.filter(carrera_jurisdiccional=carrera_jurisdiccional,
            primera_cohorte_autorizada=2008, ultima_cohorte_autorizada=2050)) == 0:
            carrera_cohorte.save()
        return cohorte

    def create_cohorte_ue(self, cohorte, ue, inscriptos):
        if ue.__class__ is Establecimiento:
            q = CohorteEstablecimiento.objects.filter(establecimiento=ue, cohorte=cohorte)
            if len(q) == 0:
                cohorte_ue = CohorteEstablecimiento()
            else:
                cohorte_ue = q[0]
            cohorte_ue.establecimiento = ue
            cohorte_ue.estado  = EstadoCohorteEstablecimiento.objects.get(nombre=EstadoCohorteEstablecimiento.REGISTRADA)
            #cohorte.establecimientos.add(ue)
            #cohorte.save()
        elif ue.__class__ is Anexo:
            q = CohorteAnexo.objects.filter(anexo=ue, cohorte=cohorte)
            if len(q) == 0:
                cohorte_ue = CohorteAnexo()
            else:
                cohorte_ue = q[0]
            cohorte_ue.anexo = ue
            cohorte_ue.estado  = EstadoCohorteAnexo.objects.get(nombre=EstadoCohorteAnexo.REGISTRADA)
            #cohorte.anexos.add(ue)
            #cohorte.save()
        elif ue.__class__ is ExtensionAulica:
            q = CohorteExtensionAulica.objects.filter(extension_aulica=ue, cohorte=cohorte)
            if len(q) == 0:
                cohorte_ue = CohorteExtensionAulica()
            else:
                cohorte_ue = q[0]
            cohorte_ue.extension_aulica = ue
            cohorte_ue.estado  = EstadoCohorteExtensionAulica.objects.get(nombre=EstadoCohorteExtensionAulica.REGISTRADA)
            #cohorte.extensiones_aulicas.add(ue)
            #cohorte.save()
        cohorte_ue.cohorte = cohorte
        cohorte_ue.inscriptos = inscriptos
        cohorte_ue.save()
        cohorte_ue.registrar_estado()
        return cohorte_ue

    def create_seguimiento(self, cohorte_ue, anio, seguimiento):
        if cohorte_ue.__class__ is CohorteEstablecimiento:
            reg_seg = CohorteEstablecimientoSeguimiento()
            reg_seg.cohorte_establecimiento = cohorte_ue
        elif cohorte_ue.__class__ is CohorteAnexo:
            reg_seg = CohorteAnexoSeguimiento()
            reg_seg.cohorte_anexo = cohorte_ue
        elif cohorte_ue.__class__ is CohorteExtensionAulica:
            reg_seg = CohorteExtensionAulicaSeguimiento()
            reg_seg.cohorte_extension_aulica = cohorte_ue
        reg_seg.anio = anio
        reg_seg.solo_cursan_nuevas_unidades = seguimiento[0]
        reg_seg.solo_recursan_nuevas_unidades = seguimiento[1]
        reg_seg.recursan_cursan_nuevas_unidades = seguimiento[2]
        reg_seg.no_cursan = seguimiento[3]
        reg_seg.egresados = seguimiento[4]
        reg_seg.save()
        return reg_seg
