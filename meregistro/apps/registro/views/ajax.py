# -*- coding: UTF-8 -*-

from django.http import HttpResponse
from apps.registro.models import Establecimiento, Departamento, Localidad, Jurisdiccion, Anexo, ExtensionAulica, DependenciaFuncional, TipoGestion
from apps.seguridad.models import Ambito
from apps.seguridad.decorators import login_required, credential_required
import simplejson as json
from django.core import serializers


@login_required
def get_localidades_por_departamento(request, departamento_id):
    localidades = Localidad.objects.filter(departamento__id=departamento_id).order_by('nombre')
    json_localidades = serializers.serialize("json", localidades)
    return HttpResponse(json_localidades, mimetype = "application/javascript")

@login_required
def get_departamentos_por_jurisdiccion(request, jurisdiccion_id):
    departamentos = Departamento.objects.filter(jurisdiccion__id=jurisdiccion_id).order_by('nombre')
    json_departamentos = serializers.serialize("json", departamentos)
    return HttpResponse(json_departamentos, mimetype="application/javascript")

@login_required
def get_tipo_gestion_de_dependencia(request, dependencia_funcional_id):
    if dependencia_funcional_id == '0':
        return HttpResponse('', mimetype="application/javascript")
    dependencia = DependenciaFuncional.objects.get(pk=dependencia_funcional_id)
    json_tipo_gestion = json.dumps(dependencia.tipo_gestion.nombre)
    return HttpResponse(json_tipo_gestion, mimetype="application/javascript")
    
@login_required
def get_tipo_gestion_de_establecimiento(request, establecimiento_id):
    if establecimiento_id == '0':
        return HttpResponse('', mimetype="application/javascript")
    dependencia = Establecimiento.objects.get(pk=establecimiento_id).dependencia_funcional
    json_tipo_gestion = json.dumps(dependencia.tipo_gestion.nombre)
    return HttpResponse(json_tipo_gestion, mimetype="application/javascript")
    
@login_required
def get_cue_parts_from_sede(request, sede_id):
    try:
        sede = Establecimiento.objects.get(pk=sede_id)
        parts = Establecimiento.get_parts_from_cue(sede.cue)
    except Establecimiento.DoesNotExist:
        parts = {'codigo_jurisdiccion': '--', 'cue': '-----', 'codigo_tipo_unidad_educativa': '--', }
    json_cue_parts = json.dumps(parts)
    return HttpResponse(json_cue_parts, mimetype="application/javascript")

@login_required
@credential_required('reg_establecimiento_verificar_datos')
def verificar_dato_establecimiento(request, establecimiento_id):
    establecimiento = Establecimiento.objects.get(pk=establecimiento_id)
    verificacion = establecimiento.get_verificacion_datos()
    value = request.GET['verificado'] == 'true'
    if request.GET['dato'] == 'domicilios':
        verificacion.domicilios = value
    elif request.GET['dato'] == 'autoridades':
        verificacion.autoridades = value
    elif request.GET['dato'] == 'turnos':
        verificacion.turnos = value
    elif request.GET['dato'] == 'matricula':
        verificacion.matricula = value
    verificacion.save()
    return HttpResponse('ok')
    

@login_required
@credential_required('reg_anexo_verificar_datos')
def verificar_dato_anexo(request, anexo_id):
    anexo = Anexo.objects.get(pk=anexo_id)
    verificacion = anexo.get_verificacion_datos()
    value = request.GET['verificado'] == 'true'
    if request.GET['dato'] == 'domicilios':
        verificacion.domicilios = value
    elif request.GET['dato'] == 'autoridades':
        verificacion.autoridades = value
    elif request.GET['dato'] == 'turnos':
        verificacion.turnos = value
    elif request.GET['dato'] == 'matricula':
        verificacion.matricula = value
    verificacion.save()
    return HttpResponse('ok')

@login_required
@credential_required('reg_extension_aulica_verificar_datos')
def verificar_dato_extension_aulica(request, extension_aulica_id):
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)
    verificacion = extension_aulica.get_verificacion_datos()
    value = request.GET['verificado'] == 'true'
    if request.GET['dato'] == 'domicilios':
        verificacion.domicilios = value
    elif request.GET['dato'] == 'autoridades':
        verificacion.autoridades = value
    elif request.GET['dato'] == 'turnos':
        verificacion.turnos = value
    elif request.GET['dato'] == 'matricula':
        verificacion.matricula = value
    verificacion.save()
    return HttpResponse('ok')
