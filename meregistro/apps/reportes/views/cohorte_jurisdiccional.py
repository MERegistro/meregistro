# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models import Carrera, CarreraJurisdiccional, CarreraJurisdiccionalCohorte
import csv
from apps.reportes.models import Reporte


@login_required
#@credential_required('tit_cohorte_jurisdiccional_consulta')
def cohortes_jurisdiccionales(request, q):
	filename = 'cohortes_jurisdiccionales_' + str(date.today()) + '.xls'
	reporte = Reporte(headers=['CARRERA', 'JURISDICCIÓN', 'COHORTES GENERADAS', 'ESTADO'], filename=filename)
	for cj in q:
		cohortes_generadas = ' - '.join("%s" % c.anio for c in cj.cohortes.all().order_by('anio'))
		if cj.estado is None:
			estado_nombre = ''
		else:
			estado_nombre = cj.estado.nombre.encode('utf8')
		reporte.rows.append([cj.carrera.nombre.encode('utf8'), cj.jurisdiccion.nombre, cohortes_generadas, estado_nombre])

	return reporte.as_csv()
