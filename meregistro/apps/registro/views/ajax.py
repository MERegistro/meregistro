# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from apps.registro.models import Establecimiento, Departamento, Localidad, Jurisdiccion
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required
import simplejson as json
from django.core import serializers


@login_required
def get_localidades_por_departamento(request, departamento_id):
    localidades = Localidad.objects.filter(departamento__id = departamento_id).order_by('nombre')
    json_localidades = serializers.serialize("json", localidades)
    return HttpResponse(json_localidades, mimetype = "application/javascript")

@login_required
def get_departamentos_por_jurisdiccion(request, jurisdiccion_id):
    departamentos = Departamento.objects.filter(jurisdiccion__id = jurisdiccion_id).order_by('nombre')
    json_departamentos = serializers.serialize("json", departamentos)
    return HttpResponse(json_departamentos, mimetype = "application/javascript")
    
@login_required
def get_cue_parts_from_sede(request, sede_id):
    try:
        sede = Establecimiento.objects.get(pk=sede_id)
        parts = Establecimiento.get_parts_from_cue(sede.cue)
    except Establecimiento.DoesNotExist:
        parts = {'codigo_jurisdiccion': '--', 'cue': '-----', 'codigo_tipo_unidad_educativa': '--', }
    json_cue_parts = json.dumps(parts)
    return HttpResponse(json_cue_parts, mimetype = "application/javascript")
