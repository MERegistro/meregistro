# -*- coding: utf-8 -*-

from apps.registro.models import Anexo, Establecimiento
from apps.titulos.models import Carrera, EstadoCarrera, TituloNacional, \
 NormativaNacional, EstadoNormativaNacional, EstadoTituloNacional
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

FIELD_SEPARATOR = '^'


class Command(BaseCommand):
    args = '<csv_file>'
    help = 'Migra una planilla de titulos jurisdiccionales'

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
        return {'id_infd': fields[0],
            'cue_anexo': fields[1],
            'titulo': fields[2],
            'primera_cohorte': fields[3],
            'ultima_cohorte': fields[4],
            'nro_infd': fields[5],
            'carrera': fields[6],
            'nro_normativa': fields[7],
            'nro_res_nac': fields[8]}

    def migrar(self, registro, reg_num):
        ue = self.find_unidad_educativa(registro['cue_anexo'])
        jurisdiccion = self.get_ue_jurisdiccion(ue)
        carrera = self.asociar_carrera_jurisdiccion(registro['carrera'], jurisdiccion)
        normativa_nacional = self.get_normativa_nacional(registro['nro_res_nac'])
        titulo_nacional = self.get_titulo_nacional(carrera, registro['titulo'], normativa_nacional)
        titulo_jurisdiccional = self.create_titulo_jurisdiccional(ue,
            titulo_nacional, registro['nro_infd'], registro['id_infd'],
            registro['nro_normativa'])
        #titulo jurisdiccional
        #asociar normativa
        #marcar que esta UE OFERTA la carrera
        
        

    def find_unidad_educativa(self, cue):
        for cls in [Anexo, Establecimiento]:
            q = cls.objects.filter(cue=cue)
            if len(q) > 0:
                return q[0]
        raise Exception("Unidad Educativa no encontrada cue:" + str(cue))


    def get_ue_jurisdiccion(self, ue):
        if ue.__class__ is Establecimiento:
            return ue.dependencia_funcional.jurisdiccion
        elif ue.__class__ is Anexo:
            return ue.establecimiento.dependencia_funcional.jurisdiccion
        raise Exception("Clase de UE invalida")


    def asociar_carrera_jurisdiccion(self, carrera_nombre, jurisdiccion):
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
        carrera.jurisdicciones.add(jurisdiccion)
        return carrera



    def get_normativa_nacional(self, numero):
        q = NormativaNacional.objects.filter(numero=numero)
        if len(q) == 0:
            normativa = NormativaNacional()
            normativa.numero = numero
            normativa.estado = EstadoNormativaNacional.objects.get(nombre=EstadoNormativaNacional.VIGENTE)
            normativa.save()
        else:
            normativa = q[0]
        return normativa


    def get_titulo_nacional(self, carrera, titulo_nombre, normativa):
        q = TituloNacional.objects.filter(nombre=titulo_nombre)
        q = q.filter(normativa_nacional=normativa)
        if len(q) == 0:
            # crear titulo nacional
            titulo = TituloNacional()
            titulo.nombre = titulo_nombre
            titulo.estado = EstadoTituloNacional.objects.get(nombre=EstadoTituloNacional.VIGENTE)
            titulo.normativa_nacional = normativa
            titulo.save()
            titulo.registrar_estado()
        else:
            titulo = q[0]
        titulo.carreras.add(carrera)
        return titulo
