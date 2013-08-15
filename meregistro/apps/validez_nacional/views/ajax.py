# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from apps.titulos.models import TituloNacional, EstadoTituloNacional, CarreraJurisdiccional
from apps.validez_nacional.models import ValidezNacional
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required
import simplejson as json
from django.core import serializers

	
@login_required
def get_titulos_por_carrera(request, carrera_id):
	
	if int(carrera_id) > 0:
		try:
			titulos = TituloNacional.objects.filter(carreras__id=carrera_id, estado__nombre=EstadoTituloNacional.VIGENTE)
		except TituloNacional.DoesNotExist:
			titulos = TituloNacional.objects.none()
	
	else:
		#titulos = TituloNacional.objects.all(estado__nombre=EstadoTituloNacional.VIGENTE)
		titulos = TituloNacional.objects.none()
	
	titulos.order_by('nombre')
	titulos = [{'pk':t.pk, 'nombre':t.nombre} for t in titulos]
	
	return HttpResponse(json.dumps(titulos), mimetype="application/javascript")


@login_required
def chequear_nro_infd(request, validez_id, nro_infd):
	
	repetido = ValidezNacional.objects.filter(nro_infd=nro_infd).exclude(pk=validez_id).exists()
	return HttpResponse(json.dumps(repetido), mimetype="application/javascript")
