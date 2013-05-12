# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models.NormativaJurisdiccional import NormativaJurisdiccional
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('tit_nor_jur_consulta')
def normativas_jurisdiccionales(request, q):
    filename = 'normativas_jurisdiccionales_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=['NUMERO/AÑO', 'TIPO', 'JURISDICCION', 'OTORGADA POR', 'OBSERVACIONES', 'ESTADO'], filename=filename)
    for nj in q:
        if nj.estado is None:
            estado_nombre = ''
        else:
            estado_nombre = nj.estado.nombre.encode('utf8')
        reporte.rows.append([nj.numero_anio.encode('utf8'), unicode(nj.tipo_normativa_jurisdiccional), unicode(nj.jurisdiccion), unicode(nj.otorgada_por), nj.observaciones.encode('utf8'), estado_nombre])
    return reporte.as_csv()
