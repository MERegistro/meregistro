# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models.Carrera import Carrera
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('tit_carrera_consulta')
def carreras(request, q):
	filename = 'carreras_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['NOMBRE', 'JURISDICCIONES', 'OBSERVACIONES', 'FECHA DE ALTA', 'ESTADO'], filename=filename)
	for carrera in q:
		if carrera.estado is None:
			estado_nombre = ''
		else:
			estado_nombre = carrera.estado.nombre.encode('utf8')
		jurisdicciones = ' - '.join("%s" % (j.nombre.encode('utf8')) for j in carrera.jurisdicciones.all())
		reporte.rows.append([carrera.nombre.encode('utf8'), jurisdicciones, carrera.observaciones.encode('utf8'), carrera.fecha_alta.strftime("%d/%m/%Y"), estado_nombre])

	return reporte.as_csv()
