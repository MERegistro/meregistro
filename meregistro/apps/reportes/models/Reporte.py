# -*- coding: utf-8 -*-

from django.http import HttpResponse
from datetime import datetime, date
import csv
import xlsxwriter
import cStringIO
import codecs
import xlwt
import tempfile
import os
"""
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
"""
class Reporte():
    def __init__(self, headers=[], filename=None):
        self.headers = headers
        self.rows = []
        self.filename = filename
        self.response = None

    def as_csv(self):
        filename = self.filename
        if filename is None:
            filename = str(date.today()) + '.xls'
        self.response = HttpResponse(mimetype='application/excel;')
        self.response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        wbk = xlwt.Workbook(encoding='utf-8')
        sheet = wbk.add_sheet('sheet 1')
        colIdx = 0
        for c in self.headers:
            sheet.write(0, colIdx, c)
            colIdx += 1
        rowIdx = 1
        for row in self.rows:
            colIdx = 0
            for c in row:
                sheet.write(rowIdx, colIdx, c)
                colIdx += 1
            rowIdx += 1
        fp, file_name = tempfile.mkstemp('.xls')
        os.close(fp)
        wbk.save(file_name)
        f = open(file_name, 'rb')
        self.response.write(f.read())
        f.close()
        os.remove(file_name)
        return self.response
        

    def as_xlsx(self):
        
        output = cStringIO.StringIO()

        book = xlsxwriter.Workbook(output)
        sheet = book.add_worksheet()
        
        rowIdx = 0
        colIdx = 0
        for c in self.headers:
            sheet.write(rowIdx, colIdx, c)
            colIdx += 1
        
        rowIdx = 1
        for row in self.rows:
            colIdx = 0
            for c in row:
                sheet.write(rowIdx, colIdx, c)
                colIdx += 1
            rowIdx += 1
        
        book.close()

        # construct response
        output.seek(0)
        filename = self.filename
        if filename is None:
            filename = str(date.today()) + '.xlsx'
        #response = HttpResponse(output.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response = HttpResponse(output.read(), mimetype='application/excel;')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        return response
        
    @classmethod
    def build_export_url(cls, url):
        has_parameters = url.find('?') > -1
        export_url = url
        if has_parameters:
            export_url += '&export=1'
        else:
            export_url += '?export=1'
        return export_url


    @staticmethod
    def dictfetchall(cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]


    @staticmethod
    def get_sql_file_content(filename):
        import os, meregistro
        queries_dir = meregistro.__path__[0] + '/apps/reportes/queries/'
        with open(queries_dir + filename, 'r') as f:
            return f.read()
