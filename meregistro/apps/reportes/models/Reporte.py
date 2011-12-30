# -*- coding: utf-8 -*-

from django.http import HttpResponse
from datetime import datetime, date
import csv

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
	self.response = HttpResponse(mimetype='text/csv')
	self.response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
	writer = csv.writer(self.response)
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
