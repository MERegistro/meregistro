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
	reporte = Reporte(headers=['NOMBRE', 'FECHA ALTA', 'TURNOS', 'TELÉFONO', 'MAIL'], filename=filename)
	for anexo in q:
		fecha = anexo.fecha_alta.strftime('%d/%m/%Y')
		turnos = ' - '.join("%s" % (t.nombre.encode('utf8')) for t in anexo.turnos.all())
		if anexo.email is None:
			email = ''
		else:
			email = anexo.email
		if anexo.telefono is None:
			telefono = ''
		else:
			telefono = anexo.telefono
		reporte.rows.append([anexo.nombre.encode('utf8'), fecha.encode('utf8'), turnos, telefono.encode('utf8'), email.encode('utf8')])
	return reporte.as_csv()
