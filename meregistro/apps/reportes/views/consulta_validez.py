# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
import csv
from apps.reportes.models import Reporte


def consulta_validez(request, q):
	filename = 'validez_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['JURISDICCIÓN', 'CUE', 'CARRERA', 'TITULO', 'PRIMERA', 'ULTIMA', 'NORMATIVA_JURISDICCIONAL', 'NORMATIVA_NACIONAL', 'NRO_INFD'], filename=filename)
	for t in q:
		reporte.rows.append([t.unidad_educativa.jurisdiccion.nombre.encode('utf8'),\
		t.unidad_educativa.cue + t.unidad_educativa.nombre, t.carrera.encode('utf8'),
		t.denominacion.encode('utf8'), t.primera.encode('utf8'), t.ultima.encode('utf8'),
		t.normativa_jurisdiccional.encode("utf8"), t.normativa_nacional.encode("utf8"),
		t.nroinfd])

	return reporte.as_csv()
