# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.DependenciaFuncional import DependenciaFuncional
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reportes_listado_dependencias_funcionales')
def dependencias_funcionales(request, q):
	filename = 'dependencias_funcionales_' + str(date.today()) + '.csv'
	reporte = Reporte(headers=['NOMBRE', 'TIPO DE GESTIÓN', 'TIPO DE DEPENDENCIA'], filename=filename)
	for dep in q:
		reporte.rows.append([dep.nombre.encode('utf8'), dep.tipo_gestion.nombre.encode('utf8'), dep.tipo_dependencia_funcional.nombre.encode('utf8')])
	return reporte.as_csv()
