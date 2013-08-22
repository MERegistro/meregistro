# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
import csv
from apps.reportes.models import Reporte


def oferta_nacional(request, q, anio):
	filename = 'oferta_nacional_' + str(anio) + '_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['JURISDICCIÓN', 'CUE', 'NOMBRE DEL ISFD', 'CARRERA', 'DOMICILIO', 'DEPARTAMENTO', 'LOCALIDAD', 'EMAIL', 'SITIO WEB'], filename=filename)
	for t in q:
		
		dom = t.establecimiento.get_domicilio_institucional()
		
		reporte.rows.append([
			t.establecimiento.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),
			t.establecimiento.cue,
			t.establecimiento.nombre,
			t.cohorte.carrera_jurisdiccional.carrera.nombre.encode('utf8'),
			str(dom),
			str(dom.localidad.departamento),
			str(dom.localidad),
			t.establecimiento.email,
			t.establecimiento.sitio_web
		])

	return reporte.as_csv()
