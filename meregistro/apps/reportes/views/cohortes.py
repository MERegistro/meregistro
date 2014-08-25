# -*- coding: UTF-8 -*-


from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from django.db import connection
from datetime import date
import csv
from apps.reportes.models import Reporte


ITEMS_PER_PAGE = 100000


@login_required
@credential_required('reportes_seguimiento_cohortes')
def seguimiento(request):
    ambito = request.get_perfil().ambito
    sql = Reporte.get_sql_file_content('417_seguimiento_cohortes.sql').replace('{{AMBITO_PATH}}', "'" + str(ambito.path) + "%%'")
    
    cursor = connection.cursor()
    cursor.execute(sql)

    filename = 'seguimiento_cohortes_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=[\
        'JURISDICCIÓN',\
        'GESTIÓN',\
        'CLAVE',\
        'TIPO',\
        'CUE',\
        'ESTABLECIMIENTO',\
        'CARRERA',\
        'COHORTE',\
        'CURSADA',\
        'INSCRIPTOS',\
        'SOLO CURSAN NUEVAS UNIDADES',\
        'SOLO RECURSAN NUEVAS UNIDADES',\
        'RECURSAN Y CURSAN NUEVAS UNIDADES',\
        'NO CURSAN',\
        'EGRESADOS',\
        'INICIAL',\
        'CONTÍNUA',\
        'INVESTIGACIÓN',\
        'APOYO',\
        'INICIAL',\
        'PRIMARIA',\
        'MEDIA',\
        'SUPERIOR'\
    ], filename=filename)
    for row in Reporte.dictfetchall(cursor):
        reporte.rows.append([\
            row['jurisdiccion'].encode('utf8') if row['jurisdiccion'] else '',\
            row['gestion'].encode('utf8') if row['gestion'] else '',\
            row['clave'] if row['clave'] else '',\
            row['tipo'].encode('utf8') if row['tipo'] else '',\
            row['cue'].encode('utf8') if row['cue'] else '',\
            row['establecimiento'].encode('utf8') if row['establecimiento'] else '',\
            row['carrera'].encode('utf8') if row['carrera'] else '',\
            row['cohorte'] if row['cohorte'] else '',\
            row['cursada'] if row['cursada'] else '',\
            row['inscriptos'] if row['inscriptos'] else '',\
            row['solo_cursan_nuevas_unidades'] if row['solo_cursan_nuevas_unidades'] else '',\
            row['solo_recursan_nuevas_unidades'] if row['solo_recursan_nuevas_unidades'] else '',\
            row['recursan_cursan_nuevas_unidades'] if row['recursan_cursan_nuevas_unidades'] else '',\
            row['no_cursan'] if row['no_cursan'] else '',\
            row['egresados'] if row['egresados'] else '',\
            row['inicial'].encode('utf8') if row['inicial'] else '',\
            row['continua'].encode('utf8') if row['continua'] else '',\
            row['investigacion'].encode('utf8') if row['investigacion'] else '',\
            row['apoyo'].encode('utf8') if row['apoyo'] else '',\
            row['inicial'].encode('utf8') if row['inicial'] else '',\
            row['primaria'].encode('utf8') if row['primaria'] else '',\
            row['media'].encode('utf8') if row['media'] else '',\
            row['superior'].encode('utf8') if row['superior'] else ''\
        ])
    return reporte.as_csv()
