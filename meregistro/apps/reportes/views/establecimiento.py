# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reportes_listado_establecimientos')
def establecimientos(request, q):
	filename = 'establecimientos_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['REGION', 'JURISDICCIÓN', 'CUE', 'DEPENDENCIA FUNCIONAL', 'NOMBRE', 'DEPARTAMENTO', 'LOCALIDAD', 'ESTADO'], filename=filename)
	for est in q:
		try:
			localidad = est.get_first_domicilio().localidad
			departamento = localidad.departamento.nombre
			localidad = localidad.nombre
		except AttributeError:
			localidad = ''
			departamento = ''
		if est.estado is None:
			estado_nombre = ''
		else:
			estado_nombre = est.estado.nombre.encode('utf8')
		reporte.rows.append([est.dependencia_funcional.jurisdiccion.region.nombre.encode('utf8'), est.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),\
		est.cue, est.dependencia_funcional.nombre.encode('utf8'), est.nombre.encode('utf8'), departamento.encode('utf8'), localidad.encode('utf8'), estado_nombre])

	return reporte.as_csv()
