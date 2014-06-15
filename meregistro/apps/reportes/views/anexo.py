# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reg_anexo_consulta')
def anexos(request, q):
   
	filename = 'anexos_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['REGION', 'JURISDICCIÓN', 'CUE', 'DEPENDENCIA FUNCIONAL', 'NOMBRE', 'DEPARTAMENTO', 'LOCALIDAD', 'ESTADO', 'VERIFICADO'], filename=filename)
	for anexo in q:
		try:
			localidad = anexo.get_first_domicilio().localidad
			departamento = localidad.departamento.nombre
			localidad = localidad.nombre
		except AttributeError:
			localidad = ''
			departamento = ''
		if anexo.estado is None:
			estado_nombre = ''
		else:
			estado_nombre = anexo.estado.nombre.encode('utf8')
		reporte.rows.append([anexo.establecimiento.dependencia_funcional.jurisdiccion.region.nombre.encode('utf8'), anexo.establecimiento.dependencia_funcional.jurisdiccion.nombre.encode('utf8'),\
		anexo.cue, anexo.establecimiento.dependencia_funcional.nombre.encode('utf8'), anexo.nombre.encode('utf8'), departamento.encode('utf8'), localidad.encode('utf8'), estado_nombre,
    "SI" if anexo.verificado() else "NO"])
    
	return reporte.as_csv()
