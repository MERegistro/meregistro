# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reg_establecimiento_consulta')
def unidades_educativas(request, q):
    filename = 'unidades_educativas_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=['REGION', 'JURISDICCIÓN', 'TIPO UNIDAD DE SERVICIO', 'CUE', 'DEPENDENCIA FUNCIONAL', 'NOMBRE', 'DEPARTAMENTO', 'LOCALIDAD', 'HISTORIAL DE ESTADOS', 'VERIFICADO'], filename=filename)
    for ue in q:
        try:
            localidad = ue.get_first_domicilio().localidad
            departamento = localidad.departamento.nombre
            localidad = localidad.nombre
        except AttributeError:
            localidad = ''
            departamento = ''
        estados = ue.registro_estados if ue.tipo_ue == 'Sede' else ue.estados.all()
        estados_out = ', '.join([e.fecha.strftime("(%d/%m/%Y)") + ' ' + e.estado.nombre for e in estados])
        reporte.rows.append([ue.dependencia_funcional.jurisdiccion.region.nombre.encode('utf8'), ue.dependencia_funcional.jurisdiccion.nombre.encode('utf8'), ue.tipo_ue, \
        ue.cue, ue.dependencia_funcional.nombre.encode('utf8'), ue.nombre.encode('utf8'), departamento.encode('utf8'), localidad.encode('utf8'), estados_out,
    "SI" if ue.verificado() else "NO"])

    return reporte.as_csv()
