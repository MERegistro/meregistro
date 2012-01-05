# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('reportes_listado_usuarios')
def usuarios(request, q):
	filename = 'usuarios_' + str(date.today()) + '.csv'
	reporte = Reporte(headers=['DOCUMENTO', 'APELLIDO', 'NOMBRE', 'PERFILES'], filename=filename)
	for usuario in q:
		perfil = ''
		perfiles_tmp = []
		for p in usuario.perfiles.all():
			fecha = p.fecha_asignacion.strftime("%d/%m/%Y")
			try:
				fecha_desasignacion = ' al ' + p.fecha_desasignacion.strftime("%d/%m/%Y")
				fecha += fecha_desasignacion
			except AttributeError:
				pass 
			perfil = '%s (%s) Asignado desde %s' % (p.rol, p.ambito, fecha,) 
			perfiles_tmp.append(perfil)
		perfiles = '\n'.join("%s" % (p) for p in perfiles_tmp)
		reporte.rows.append([usuario.tipo_documento.abreviatura + ': ' + usuario.documento, usuario.apellido.encode('utf8'), usuario.nombre.encode('utf8'), perfiles])
	return reporte.as_csv()
