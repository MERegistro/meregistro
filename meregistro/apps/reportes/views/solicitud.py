# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
import csv
from apps.reportes.models import Reporte


@login_required
def detalle_numeracion(request, validez):
	filename = 'detalle_numeracion_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['TIPO UE', 'CUE', 'NOMBRE DE LA UE', 'DEPARTAMENTO', 'LOCALIDAD', 'NRO INFD'], filename=filename)

	for v in validez:
		nombre_ue = v.get_unidad_educativa().nombre.encode('utf8')
		departamento = str(v.get_unidad_educativa().get_domicilio_institucional().localidad.departamento)
		localidad = str(v.get_unidad_educativa().get_domicilio_institucional().localidad)
		reporte.rows.append([v.tipo_unidad_educativa.encode('utf8'), v.cue, nombre_ue, departamento, localidad, v.nro_infd])

	return reporte.as_csv()
