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
	reporte = Reporte(headers=['NOMBRE', 'FECHA ALTA', 'TURNOS', 'TELÉFONO', 'MAIL', 'VERIFICADO'], filename=filename)
	for extension_aulica in q:
		fecha = '' if extension_aulica.fecha_alta is None else extension_aulica.fecha_alta.strftime('%d/%m/%Y')
		turnos = '' #' - '.join("%s" % (t.nombre.encode('utf8')) for t in extension_aulica.turnos.all())
		if extension_aulica.email is None:
			email = ''
		else:
			email = extension_aulica.email
		if extension_aulica.telefono is None:
			telefono = ''
		else:
			telefono = extension_aulica.telefono
		reporte.rows.append([extension_aulica.nombre.encode('utf8'), fecha, turnos, telefono.encode('utf8'), email.encode('utf8'),
    "SI" if extension_aulica.verificado() else "NO"])
	return reporte.as_csv()
