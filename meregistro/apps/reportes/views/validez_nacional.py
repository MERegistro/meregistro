# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
import csv
from apps.reportes.models import Reporte


@login_required
def solicitudes(request, q):
	filename = 'solicitudes_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['JURISDICCIÓN', 'CARRERA', 'TÍTULO', 'NORMATIVAS JURISDICCIONALES.', 'CUE', 'COHORTES', 'ESTADO', 'DICTAMEN COFEV', 'NORMATIVAS NACIONALES'], filename=filename)
	
	for sol in q:
		
		normativas_jurisdiccionales = ", ".join(sol.normativas_jurisdiccionales.all()) or "---"
		cues = "cues"
		
		try:
			dictamen_cofev = sol.dictamen_cofev.encode('utf8')
		except AttributeError:
			dictamen_cofev = "---"
			
		try:
			normativas_nacionales = sol.normativas_nacionales.encode('utf8')
		except AttributeError:
			normativas_nacionales = "---"
			
		reporte.rows.append([sol.jurisdiccion.nombre.encode('utf8'), sol.carrera.nombre.encode('utf8'), sol.titulo_nacional.nombre.encode('utf8'),\
		normativas_jurisdiccionales, cues, (sol.primera_cohorte or "--- ") + '/' + (sol.ultima_cohorte or " ---"), sol.estado.nombre.encode('utf8'), dictamen_cofev, normativas_nacionales])

	return reporte.as_csv()
