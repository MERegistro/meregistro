# -*- coding: utf-8 -*-

from django.db import connection
from apps.reportes.models import Reporte

class Estadistica():

    @classmethod
    def datos_generales(cls):
        sql = Reporte.__get_sql_file_content('datos_generales.sql')
        cursor = connection.cursor()

        cursor.execute(sql)
        return cls.__dictfetchall(cursor)
