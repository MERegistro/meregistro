# -*- coding: utf-8 -*-

from django.http import HttpResponse
from datetime import datetime, date
import csv
import cStringIO
import codecs

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
            filename = str(date.today()) + '.csv'
        self.response = HttpResponse(mimetype='text/csv; charset=utf-8')
        self.response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
        writer = csv.writer(self.response, delimiter=';')
        writer.writerow(self.headers)
        for row in self.rows:
            writer.writerow(row)
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
