# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.ExtensionAulica import ExtensionAulica
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reg_extension_aulica_consulta')
def extensiones_aulicas(request, q):

	filename = 'extensiones_aulicas_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['REGION', 'JURISDICCIÓN', 'CUE', 'DEPENDENCIA FUNCIONAL', 'NOMBRE', 'DEPARTAMENTO', 'LOCALIDAD', 'ESTADO', 'VERIFICADO'], filename=filename)
	for ea in q:
		try:
			localidad = ea.get_first_domicilio().localidad
			departamento = localidad.departamento.nombre
			localidad = localidad.nombre
		except AttributeError:
			localidad = ''
			departamento = ''
		if ea.estado is None:
			estado_nombre = ''
		else:
			estado_nombre = ea.estado.nombre.encode('utf8')
		reporte.rows.append([ea.establecimiento.dependencia_funcional.jurisdiccion.region.nombre.encode('utf8'), ea.establecimiento.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),\
		ea.cue, ea.establecimiento.dependencia_funcional.nombre.encode('utf8'), ea.nombre.encode('utf8'), departamento.encode('utf8'), localidad.encode('utf8'), estado_nombre,
    "SI" if ea.verificado() else "NO"])

	return reporte.as_csv()
