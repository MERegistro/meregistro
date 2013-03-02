# -*- coding: UTF-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime, date
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
import csv
from apps.reportes.models import Reporte


@login_required
@credential_required('seg_usuario_buscar')
def usuarios(request, q):
  filename = 'usuarios_' + str(date.today()) + '.xls'
  headers = ['DOCUMENTO', 'APELLIDO', 'NOMBRE', 'PERFILES']
  if request.has_credencial('seg_ver_datos_acceso'):
    headers.append('Accesos')
    headers.append('Último Acceso')
  reporte = Reporte(headers=headers, filename=filename)
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
    new_row = [usuario.tipo_documento.abreviatura + ': ' + usuario.documento, usuario.apellido.encode('utf8'), usuario.nombre.encode('utf8'), perfiles]
    if request.has_credencial('seg_ver_datos_acceso'):
      new_row.append(usuario.logins_count)
      if usuario.last_login is None:
        new_row.append('')
      else:
        new_row.append(usuario.last_login.strftime("%d/%m/%Y"))
    reporte.rows.append(new_row)
  return reporte.as_csv()
