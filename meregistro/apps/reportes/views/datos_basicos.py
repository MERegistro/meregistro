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
@credential_required('reportes_datos_basicos_sedes')
def sedes(request):

    sql = Reporte.get_sql_file_content('404_datos_basicos_sedes.sql').replace('{{AMBITO_PATH}}', "'" + str(request.get_perfil().ambito.path) + "%%'")

    cursor = connection.cursor()
    cursor.execute(sql)

    filename = 'sedes_datos_basicos_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=[\
        'JURISDICCIÓN',\
        'GESTIÓN',\
        'CUE',\
        'ESTABLECIMIENTO',\
        'TELÉFONO',\
        'EMAIL',\
        'DEP. FUNCIONAL',\
        'TM',\
        'TT',\
        'TN',\
        'CALLE INSTITUCIONAL',\
        'ALTURA',\
        'REFERENCIA',\
        'CP',\
        'LOCALIDAD',\
        'CALLE POSTAL',\
        'ALTURA', 'REFERENCIA',\
        'CP',\
        'LOCALIDAD',\
        'CONEXIÓN',\
        'COMPARTIDO',\
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
            row['cue'].encode('utf8') if row['cue'] else '',\
            row['establecimiento'].encode('utf8') if row['establecimiento'] else '',\
            row['telefono'].encode('utf8') if row['telefono'] else '',\
            row['email'].encode('utf8') if row['email'] else '',\
            row['dep_funcional'].encode('utf8') if row['dep_funcional'] else '',\
            row['tm'].encode('utf8') if row['tm'] else '',\
            row['tt'].encode('utf8') if row['tt'] else '',\
            row['tn'].encode('utf8') if row['tn'] else '',\
            row['calle_institucional'].encode('utf8') if row['calle_institucional'] else '',\
            row['altura_institucional'].encode('utf8') if row['altura_institucional'] else '',\
            row['referencia_institucional'].encode('utf8') if row['referencia_institucional'] else '',\
            row['cp_institucional'].encode('utf8') if row['cp_institucional'] else '',\
            row['localidad_institucional'].encode('utf8') if row['localidad_institucional'] else '',\
            row['calle_postal'].encode('utf8') if row['calle_postal'] else '',\
            row['altura_postal'].encode('utf8') if row['altura_postal'] else '',\
            row['referencia_postal'].encode('utf8') if row['referencia_postal'] else '',\
            row['cp_postal'].encode('utf8') if row['cp_postal'] else '',\
            row['localidad_postal'].encode('utf8') if row['localidad_postal'] else '',\
            row['conexion'].encode('utf8') if row['conexion'] else '',\
            row['compartido'].encode('utf8') if row['compartido'] else '',\
            row['inicial_funcion'].encode('utf8') if row['inicial_funcion'] else '',\
            row['continua'].encode('utf8') if row['continua'] else '',\
            row['investigacion'].encode('utf8') if row['investigacion'] else '',\
            row['apoyo'].encode('utf8') if row['apoyo'] else '',\
            row['inicial'].encode('utf8') if row['inicial'] else '',\
            row['primaria'].encode('utf8') if row['primaria'] else '',\
            row['media'].encode('utf8') if row['media'] else '',\
            row['superior'].encode('utf8') if row['superior'] else ''\
        ])
    return reporte.as_csv()


@login_required
@credential_required('reportes_datos_basicos_anexos')
def anexos(request):
    sql = Reporte.get_sql_file_content('404_datos_basicos_anexos.sql').replace('{{AMBITO_PATH}}', "'" + str(request.get_perfil().ambito.path) + "%%'")
    cursor = connection.cursor()

    cursor.execute(sql)

    filename = 'anexos_datos_basicos_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=[\
        'JURISDICCIÓN',\
        'GESTIÓN',\
        'CUE',\
        'ANEXO',\
        'TELÉFONO',\
        'EMAIL',\
        'DEP. FUNCIONAL',\
        'TM',\
        'TT',\
        'TN',\
        'CALLE INSTITUCIONAL',\
        'ALTURA',\
        'REFERENCIA',\
        'CP',\
        'LOCALIDAD',\
        'CALLE POSTAL',\
        'ALTURA', 'REFERENCIA',\
        'CP',\
        'LOCALIDAD',\
        'CONEXIÓN',\
        'COMPARTIDO',\
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
            row['cue'].encode('utf8') if row['cue'] else '',\
            row['anexo'].encode('utf8') if row['anexo'] else '',\
            row['telefono'].encode('utf8') if row['telefono'] else '',\
            row['email'].encode('utf8') if row['email'] else '',\
            row['dep_funcional'].encode('utf8') if row['dep_funcional'] else '',\
            row['tm'].encode('utf8') if row['tm'] else '',\
            row['tt'].encode('utf8') if row['tt'] else '',\
            row['tn'].encode('utf8') if row['tn'] else '',\
            row['calle_institucional'].encode('utf8') if row['calle_institucional'] else '',\
            row['altura_institucional'].encode('utf8') if row['altura_institucional'] else '',\
            row['referencia_institucional'].encode('utf8') if row['referencia_institucional'] else '',\
            row['cp_institucional'].encode('utf8') if row['cp_institucional'] else '',\
            row['localidad_institucional'].encode('utf8') if row['localidad_institucional'] else '',\
            row['calle_postal'].encode('utf8') if row['calle_postal'] else '',\
            row['altura_postal'].encode('utf8') if row['altura_postal'] else '',\
            row['referencia_postal'].encode('utf8') if row['referencia_postal'] else '',\
            row['cp_postal'].encode('utf8') if row['cp_postal'] else '',\
            row['localidad_postal'].encode('utf8') if row['localidad_postal'] else '',\
            row['conexion'].encode('utf8') if row['conexion'] else '',\
            row['compartido'].encode('utf8') if row['compartido'] else '',\
            row['inicial_funcion'].encode('utf8') if row['inicial_funcion'] else '',\
            row['continua'].encode('utf8') if row['continua'] else '',\
            row['investigacion'].encode('utf8') if row['investigacion'] else '',\
            row['apoyo'].encode('utf8') if row['apoyo'] else '',\
            row['inicial'].encode('utf8') if row['inicial'] else '',\
            row['primaria'].encode('utf8') if row['primaria'] else '',\
            row['media'].encode('utf8') if row['media'] else '',\
            row['superior'].encode('utf8') if row['superior'] else ''\
        ])
    return reporte.as_csv()
    

@login_required
@credential_required('reportes_datos_basicos_extensiones_aulicas')
def extensiones_aulicas(request):
    sql = Reporte.get_sql_file_content('404_datos_basicos_extensiones_aulicas.sql').replace('{{AMBITO_PATH}}', "'" + str(request.get_perfil().ambito.path) + "%%'")
    cursor = connection.cursor()

    cursor.execute(sql)

    filename = 'extensiones_aulicas_datos_basicos_' + str(date.today()) + '.xls'
    reporte = Reporte(headers=[\
        'JURISDICCIÓN',\
        'GESTIÓN',\
        'CUE',\
        'EXTENSION AULICA',\
        'TELÉFONO',\
        'EMAIL',\
        'DEP. FUNCIONAL',\
        'TM',\
        'TT',\
        'TN',\
        'CALLE INSTITUCIONAL',\
        'ALTURA',\
        'REFERENCIA',\
        'CP',\
        'LOCALIDAD',\
        'CALLE POSTAL',\
        'ALTURA', 'REFERENCIA',\
        'CP',\
        'LOCALIDAD',\
        'CONEXIÓN',\
        'COMPARTIDO',\
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
            row['cue'].encode('utf8') if row['cue'] else '',\
            row['extension_aulica'].encode('utf8') if row['extension_aulica'] else '',\
            row['telefono'].encode('utf8') if row['telefono'] else '',\
            row['email'].encode('utf8') if row['email'] else '',\
            row['dep_funcional'].encode('utf8') if row['dep_funcional'] else '',\
            row['tm'].encode('utf8') if row['tm'] else '',\
            row['tt'].encode('utf8') if row['tt'] else '',\
            row['tn'].encode('utf8') if row['tn'] else '',\
            row['calle_institucional'].encode('utf8') if row['calle_institucional'] else '',\
            row['altura_institucional'].encode('utf8') if row['altura_institucional'] else '',\
            row['referencia_institucional'].encode('utf8') if row['referencia_institucional'] else '',\
            row['cp_institucional'].encode('utf8') if row['cp_institucional'] else '',\
            row['localidad_institucional'].encode('utf8') if row['localidad_institucional'] else '',\
            row['calle_postal'].encode('utf8') if row['calle_postal'] else '',\
            row['altura_postal'].encode('utf8') if row['altura_postal'] else '',\
            row['referencia_postal'].encode('utf8') if row['referencia_postal'] else '',\
            row['cp_postal'].encode('utf8') if row['cp_postal'] else '',\
            row['localidad_postal'].encode('utf8') if row['localidad_postal'] else '',\
            row['conexion'].encode('utf8') if row['conexion'] else '',\
            row['compartido'].encode('utf8') if row['compartido'] else '',\
            row['inicial_funcion'].encode('utf8') if row['inicial_funcion'] else '',\
            row['continua'].encode('utf8') if row['continua'] else '',\
            row['investigacion'].encode('utf8') if row['investigacion'] else '',\
            row['apoyo'].encode('utf8') if row['apoyo'] else '',\
            row['inicial'].encode('utf8') if row['inicial'] else '',\
            row['primaria'].encode('utf8') if row['primaria'] else '',\
            row['media'].encode('utf8') if row['media'] else '',\
            row['superior'].encode('utf8') if row['superior'] else ''\
        ])
    return reporte.as_csv()
