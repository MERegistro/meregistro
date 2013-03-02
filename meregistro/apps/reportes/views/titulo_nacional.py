# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models.TituloNacional import TituloNacional
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('tit_titulo_nacional_consulta')
def titulos_nacionales(request, q):
	filename = 'titulos_nacionales_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['NORMATIVA', 'NOMBRE', 'OBSERVACIONES', 'FECHA DE ALTA', 'ESTADO'], filename=filename)
	for t in q:
		if t.estado is None:
			estado_nombre = ''
		else:
			estado_nombre = t.estado.nombre.encode('utf8')
		reporte.rows.append([t.normativa_nacional.numero.encode('utf8'), t.nombre.encode('utf8'), t.observaciones, t.fecha_alta.strftime("%d/%m/%Y"), estado_nombre])

	return reporte.as_csv()
