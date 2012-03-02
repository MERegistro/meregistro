# -*- coding: utf-8 -*-

from django.http import HttpResponse
from datetime import datetime, date
import csv
import cStringIO
import codecs
import xlwt
import tempfile
import os

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

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
        #writer = csv.writer(self.response, delimiter=';')
        #writer.writerow(self.headers)
        rowIdx = 0
        for row in self.rows:
            colIdx = 0
            for c in row:
                sheet.write(rowIdx, colIdx, c)
                colIdx += 1
            rowIdx += 1
        #    writer.writerow(row)
        fp, file_name = tempfile.mkstemp('.xls')
        os.close(fp)
        wbk.save(file_name)
        f = open(file_name, 'rb')
        self.response.write(f.read())
        f.close()
        return self.response


    @classmethod
    def build_export_url(cls, url):
        has_parameters = url.find('?') > -1
        export_url = url
        if has_parameters:
            export_url += '&export=1'
        else:
            export_url += '?export=1'
        return export_url
