# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from apps.registro.models import Establecimiento, Anexo, ExtensionAulica
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required, credential_required



@login_required
@credential_required('reg_establecimiento_verificar_datos')
def establecimiento(request):
	establecimiento_id = request.POST['unidad_educativa_id']
	dato_verificacion = request.POST['dato_verificacion']
	return_url = request.POST['return_url']
	establecimiento = Establecimiento.objects.get(pk=establecimiento_id)
	verificacion = establecimiento.get_verificacion_datos()

	try:
		verificado = request.POST['verificado'] == 'on'
	except KeyError:
		verificado = False
		
	if dato_verificacion == 'domicilios':
		verificacion.domicilios = verificado
	elif dato_verificacion == 'autoridades':
		verificacion.autoridades = verificado
	elif dato_verificacion == 'turnos':
		verificacion.turnos = verificado
	elif dato_verificacion == 'matricula':
		verificacion.matricula = verificado
	verificacion.save()

	request.set_flash('success', 'Datos guardados correctamente.')
	return HttpResponseRedirect(reverse(return_url, args=[establecimiento_id]))
