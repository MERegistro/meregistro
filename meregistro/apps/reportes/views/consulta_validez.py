# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.validez_nacional.models import ValidezNacional
import csv
from apps.reportes.models import Reporte


def consulta_validez(request, q):
	filename = 'validez_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['JURISDICCIÓN', 'CUE', 'NOMBRE DEL ISFD', 'TIPO DE GESTIÓN', 'CARRERA', 'TITULO', 'PRIMERA COHORTE', 'ULTIMA COHORTE', 'NORMATIVA_JURISDICCIONAL', 'NORMATIVA_NACIONAL', 'NRO_INFD'], filename=filename)
	for v in q:
		ue = v.get_unidad_educativa()
		if v.tipo_unidad_educativa == ValidezNacional.TIPO_UE_SEDE:
			df = ue.dependencia_funcional
		else:
			df = ue.establecimiento.dependencia_funcional

		reporte.rows.append([
		df.jurisdiccion.nombre.encode('utf8'),
		v.cue,
		ue.nombre, 
		df.tipo_gestion.nombre.encode('utf8'),
		v.carrera.encode('utf8'),
		v.titulo_nacional.encode('utf8'), 
		v.primera_cohorte.encode('utf8'), 
		v.ultima_cohorte.encode('utf8'),
		v.normativa_jurisdiccional.encode("utf8"), 
		v.normativas_nacionales.encode("utf8"),
		v.nro_infd])

	return reporte.as_csv()
