# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.validez_nacional.models import ValidezNacional
import csv
from apps.reportes.models import Reporte

"""
{'dictamen_cofev': None, 
'referencia': None,
'normativas_nacionales': u'790/05',
'_state': <django.db.models.base.ModelState object at 0x7f1b3ab4b1d0>,
'cue': u'060000600',
'titulo_nacional': u'Profesor de Arte en Teatro',
'ultima_cohorte': u'2007',
'solicitud_id': 6622,
'carrera': u'Profesorado de Teatro',
'normativa_jurisdiccional': u'1106/03; 1106/03 4664/03; 1106/03; 4664/03; 1790/03; 4664/03',
'unidad_educativa_id': 24,
'primera_cohorte': u'2001',
'nro_infd': u'0600002408T008647',
'id': 20001,
'tipo_unidad_educativa': u'Sede'}

"""
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
