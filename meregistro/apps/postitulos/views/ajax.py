# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from apps.postitulos.models import PostituloNacional, EstadoPostituloNacional, CarreraPostituloJurisdiccional
from apps.postitulos.models import ValidezNacional
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required
import simplejson as json
from django.core import serializers

    
@login_required
def get_postitulos_por_carrera(request, carrera_id):
    carrera_id = carrera_id or 0
    if int(carrera_id) > 0:
        try:
            postitulos = PostituloNacional.objects.filter(carreras__id=carrera_id, estado__nombre=EstadoPostituloNacional.VIGENTE)
        except PostituloNacional.DoesNotExist:
            postitulos = PostituloNacional.objects.none()
    else:
        postitulos = PostituloNacional.objects.none()
    
    postitulos.order_by('nombre')
    postitulos = [{'pk':t.pk, 'nombre':t.nombre} for t in postitulos]
    
    return HttpResponse(json.dumps(postitulos), mimetype="application/javascript")


@login_required
def chequear_nro_infd(request, validez_id, nro_infd):
    
    repetido = ValidezNacional.objects.filter(nro_infd=nro_infd).exclude(pk=validez_id).exists()
    return HttpResponse(json.dumps(repetido), mimetype="application/javascript")
