# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.ExtensionAulica import ExtensionAulica
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reportes_listado_extensiones_aulicas')
def extensiones_aulicas(request, q):
	filename = 'extensiones_aulicas_' + str(date.today()) + '.csv'
	reporte = Reporte(headers=['NOMBRE', 'FECHA ALTA', 'TURNOS', 'TELÉFONO', 'MAIL'], filename=filename)
	for extension_aulica in q:
		fecha = extension_aulica.fecha_alta.strftime('%d/%m/%Y')
		turnos = ' - '.join("%s" % (t.nombre.encode('utf8')) for t in extension_aulica.turnos.all())
		reporte.rows.append([extension_aulica.nombre.encode('utf8'), fecha, turnos, extension_aulica.telefono.encode('utf8'), extension_aulica.email.encode('utf8')])
	return reporte.as_csv()
