# -*- coding: UTF-8 -*-


from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from django.db import connection
from datetime import date
import csv
import xlsxwriter
from apps.reportes.models import Reporte


ITEMS_PER_PAGE = 100000


@login_required
@credential_required('reportes_seguimiento_cohortes')
def seguimiento(request):
    ambito = request.get_perfil().ambito
    sql = Reporte.get_sql_file_content('417_seguimiento_cohortes_b.sql').replace('{{AMBITO_PATH}}', "'" + str(ambito.path) + "%%'")
    
    cursor = connection.cursor()
    cursor.execute(sql)
    filename = 'seguimiento_cohortes_' + str(date.today()) + '.xlsx'
    reporte = Reporte(headers=[\
        'JURISDICCION',\
        'GESTION',\
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
        'CONTINUA',\
        'INVESTIGACION',\
        'APOYO',\
        'INICIAL',\
        'PRIMARIA',\
        'MEDIA',\
        'SUPERIOR'\
    ], filename=filename)
    for row in Reporte.dictfetchall(cursor):
        reporte.rows.append([\
            row['jurisdiccion'] if row['jurisdiccion'] else '',\
            row['gestion'] if row['gestion'] else '',\
            row['clave'] if row['clave'] else '',\
            row['tipo'] if row['tipo'] else '',\
            row['cue'] if row['cue'] else '',\
            row['establecimiento'] if row['establecimiento'] else '',\
            row['carrera'] if row['carrera'] else '',\
            row['cohorte'] if row['cohorte'] else '',\
            row['cursada'] if row['cursada'] else '',\
            row['inscriptos'] if row['inscriptos'] else '',\
            row['solo_cursan_nuevas_unidades'] if row['solo_cursan_nuevas_unidades'] else '',\
            row['solo_recursan_nuevas_unidades'] if row['solo_recursan_nuevas_unidades'] else '',\
            row['recursan_cursan_nuevas_unidades'] if row['recursan_cursan_nuevas_unidades'] else '',\
            row['no_cursan'] if row['no_cursan'] else '',\
            row['egresados'] if row['egresados'] else '',\
            row['inicial'] if row['inicial'] else '',\
            row['continua'] if row['continua'] else '',\
            row['investigacion'] if row['investigacion'] else '',\
            row['apoyo'] if row['apoyo'] else '',\
            row['inicial'] if row['inicial'] else '',\
            row['primaria'] if row['primaria'] else '',\
            row['media'] if row['media'] else '',\
            row['superior'] if row['superior'] else ''\
        ])
    return reporte.as_xlsx()
