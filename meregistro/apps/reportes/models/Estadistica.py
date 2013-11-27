# -*- coding: utf-8 -*-

from django.db import connection

class Estadistica():

    @staticmethod
    def __dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    @staticmethod
    def __get_sql_file_content(filename):
        import os, meregistro
        queries_dir = meregistro.__path__[0] + '/apps/reportes/queries/'
        with open(queries_dir + filename, 'r') as f:
            return f.read()

    @classmethod
    def datos_generales(cls):
        sql = cls.__get_sql_file_content('datos_generales.sql')
        cursor = connection.cursor()

        cursor.execute(sql)
        return cls.__dictfetchall(cursor)
