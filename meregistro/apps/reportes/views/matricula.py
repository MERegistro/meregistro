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
@credential_required('reportes_matricula')
def index(request):
    ambito = request.get_perfil().ambito
    sql = Reporte.get_sql_file_content('418_matricula.sql').replace('{{AMBITO_PATH}}', "'" + str(ambito.path) + "%%'")
    
    cursor = connection.cursor()
    cursor.execute(sql)
    filename = 'matricula_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=[\
        'JURISDICCIÓN',\
        'GESTIÓN',\
        'CLAVE',\
        'TIPO',\
        'CUE',\
        'ESTABLECIMIENTO',\
        'AÑO',\
        'PROFESORADOS',\
        'POSTÍTULOS',\
        'FORMACIÓN CONTÍNUA',\
        'FORMACIÓN DOCENTE',\
        'TECNICATURAS',\
        'TOTAL',\
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
            row['nombre'].encode('utf8') if row['nombre'] else '',\
            row['anio'] if row['anio'] else '',\
            row['profesorados'] if row['profesorados'] else '',\
            row['postitulos'] if row['postitulos'] else '',\
            row['formacion_continua'] if row['formacion_continua'] else '',\
            row['formacion_docente'] if row['formacion_docente'] else '',\
            row['tecnicaturas'] if row['tecnicaturas'] else '',\
            row['total'] if row['total'] else '',\
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
