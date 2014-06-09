# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
import csv
from apps.reportes.models import Reporte


def oferta_nacional(request, q, anio):
	filename = 'oferta_nacional_' + str(anio) + '_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['JURISDICCIÓN', 'CUE', 'NOMBRE DEL ISFD', 'CARRERA', 'DOMICILIO', 'DEPARTAMENTO', 'LOCALIDAD', 'EMAIL', 'SITIO WEB'], filename=filename)
	
	q_est = q[0]
	q_anexo = q[1]
	q_ea = q[2]

	for t in q_est:
		dom = t.establecimiento.get_domicilio_institucional()
		if not dom:
			dom = ""
			departamento = ""
			localidad = ""
		else:
			departamento = str(dom.localidad.departamento)
			localidad = str(dom.localidad)
		
		reporte.rows.append([
			t.establecimiento.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),
			t.establecimiento.cue,
			t.establecimiento.nombre,
			t.cohorte.carrera_jurisdiccional.carrera.nombre.encode('utf8'),
			str(dom),
			departamento,
			localidad,
			t.establecimiento.email,
			t.establecimiento.sitio_web
		])

	for t in q_anexo:
		dom = t.anexo.get_domicilio_institucional()
		if not dom:
			dom = ""
			departamento = ""
			localidad = ""
		else:
			departamento = str(dom.localidad.departamento)
			localidad = str(dom.localidad)
		
		reporte.rows.append([
			t.anexo.establecimiento.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),
			t.anexo.cue,
			t.anexo.nombre,
			t.cohorte.carrera_jurisdiccional.carrera.nombre.encode('utf8'),
			str(dom),
			departamento,
			localidad,
			t.anexo.email,
			t.anexo.sitio_web
		])

	for t in q_ea:
		dom = t.extension_aulica.get_domicilio_institucional()
		if not dom:
			dom = ""
			departamento = ""
			localidad = ""
		else:
			departamento = str(dom.localidad.departamento)
			localidad = str(dom.localidad)
		
		reporte.rows.append([
			t.extension_aulica.establecimiento.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),
			t.extension_aulica.cue,
			t.extension_aulica.nombre,
			t.cohorte.carrera_jurisdiccional.carrera.nombre.encode('utf8'),
			str(dom),
			departamento,
			localidad,
			t.extension_aulica.email,
			t.extension_aulica.sitio_web
		])

	return reporte.as_csv()
