# -*- coding: UTF-8 -*-

from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import simplejson as json
from django.core import serializers
import json
import datetime

@require_http_methods(["GET"])
def getOfertaPorAnio(request, anio):
    anios_disponibles = ['2013', '2014', '2015', '2016']
    if anio not in anios_disponibles:
        r = json.dumps({'error': u'Año inválido. Debe ser entre ' + anios_disponibles[0] + ' y ' + anios_disponibles[-1]}, ensure_ascii=False)
        return HttpResponse(r, mimetype = "application/javascript")

    from apps.titulos.models import Cohorte, CohorteEstablecimiento, CarreraJurisdiccional, Carrera, CohorteAnexo, CohorteExtensionAulica
    q1 = CohorteEstablecimiento.objects.filter(cohorte__anio=anio)
    q2 = CohorteAnexo.objects.filter(cohorte__anio=anio)
    q3 = CohorteExtensionAulica.objects.filter(cohorte__anio=anio)

    q1.distinct().order_by('establecimiento__dependencia_funcional__jurisdiccion__nombre', 'establecimiento__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
    q2.distinct().order_by('anexo__dependencia_funcional__jurisdiccion__nombre', 'anexo__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
    q3.distinct().order_by('extension_aulica__dependencia_funcional__jurisdiccion__nombre', 'extension_aulica__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')

    sedes = [{'Anio': ce.cohorte.anio, 'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ce.get_unidad_educativa().id, 'Instituto': ce.get_unidad_educativa().nombre, 'CueAnexo': ce.get_unidad_educativa().cue, 'IDCarrera': ce.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ce.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ce.get_establecimiento().dependencia_funcional.tipo_gestion.nombre} for ce in q1]
    anexos = [{'Anio': ca.cohorte.anio, 'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ca.get_unidad_educativa().id, 'Instituto': ca.get_unidad_educativa().nombre, 'CueAnexo': ca.get_unidad_educativa().cue, 'IDCarrera': ca.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ca.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ca.get_establecimiento().dependencia_funcional.tipo_gestion.nombre} for ca in q2]
    extensiones = [{'Anio': cea.cohorte.anio, 'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': cea.get_unidad_educativa().id, 'Instituto': cea.get_unidad_educativa().nombre, 'CueAnexo': cea.get_unidad_educativa().cue, 'IDCarrera': cea.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': cea.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': cea.get_establecimiento().dependencia_funcional.tipo_gestion.nombre} for cea in q3]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getPadronDepartamentos(request):
    from apps.registro.models import Departamento, Jurisdiccion
    q = [{'IDDepartamento': d.id, 'Departamento': d.nombre, 'IdJurisdiccion': d.jurisdiccion.id, 'PrefijoJurisdiccion': d.jurisdiccion.prefijo, 'Jurisdiccion': d.jurisdiccion.nombre} for d in Departamento.objects.all().order_by('jurisdiccion__nombre', 'nombre')]
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getDepartamentosPorJurisdiccion(request, prefijo_jurisdiccion):
    from apps.registro.models import Departamento, Jurisdiccion
    q = [{'IDDepartamento': d.id, 'Departamento': d.nombre, 'IdJurisdiccion': d.jurisdiccion.id, 'PrefijoJurisdiccion': d.jurisdiccion.prefijo, 'Jurisdiccion': d.jurisdiccion.nombre} for d in Departamento.objects.all().filter(jurisdiccion__prefijo=prefijo_jurisdiccion).order_by('jurisdiccion__nombre', 'nombre')]
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getPadronLocalidades(request):
    from apps.registro.models import Localidad, Departamento
    q = [{'IDDepartamento': l.departamento.id, 'Departamento': l.departamento.nombre, 'IDLocalidad': l.id, 'Localidad': l.nombre} for l in Localidad.objects.all().order_by('departamento__jurisdiccion__nombre', 'departamento__nombre', 'nombre')]
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getLocalidadesPorDepartamento(request, departamento_id):
    from apps.registro.models import Localidad, Departamento
    q = [{'IDDepartamento': l.departamento.id, 'Departamento': l.departamento.nombre, 'IDLocalidad': l.id, 'Localidad': l.nombre} for l in Localidad.objects.all().filter(departamento__id=departamento_id).order_by('departamento__jurisdiccion__nombre', 'departamento__nombre', 'nombre')]
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getPadronInstitutos(request):
    from apps.registro.models import Establecimiento, Anexo, ExtensionAulica

    sedes = [{'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.dependencia_funcional.tipo_gestion.nombre} for ue in Establecimiento.objects.all().order_by('cue')]
    anexos = [{'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ue in Anexo.objects.all().order_by('cue')]
    extensiones = [{'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ue in ExtensionAulica.objects.all().order_by('cue')]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getInstitutosPorLocalidad(request, localidad_id):
    from apps.registro.models import Establecimiento, Anexo, ExtensionAulica

    sedes = [{'Localidad': ue.get_domicilio_institucional().localidad.nombre, 'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.dependencia_funcional.tipo_gestion.nombre} for ue in Establecimiento.objects.filter(domicilios__tipo_domicilio__descripcion='Institucional', domicilios__localidad__id=localidad_id).all().order_by('cue')]
    anexos = [{'Localidad': ue.get_domicilio_institucional().localidad.nombre, 'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ue in Anexo.objects.filter(anexo_domicilio__tipo_domicilio__descripcion='Institucional', anexo_domicilio__localidad__id=localidad_id).all().order_by('cue')]
    extensiones = [{'Localidad': ue.get_domicilio_institucional().localidad.nombre, 'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ue in ExtensionAulica.objects.filter(domicilio__tipo_domicilio__descripcion='Institucional', domicilio__localidad__id=localidad_id).all().order_by('cue')]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getInstitutosEstatalesPorLocalidad(request, localidad_id):
    from apps.registro.models import Establecimiento, Anexo, ExtensionAulica

    sedes = [{'Localidad': ue.get_domicilio_institucional().localidad.nombre, 'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.dependencia_funcional.tipo_gestion.nombre} for ue in Establecimiento.objects.filter(dependencia_funcional__tipo_gestion__nombre='Estatal', domicilios__tipo_domicilio__descripcion='Institucional', domicilios__localidad__id=localidad_id).all().order_by('cue')]
    anexos = [{'Localidad': ue.get_domicilio_institucional().localidad.nombre, 'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ue in Anexo.objects.filter(establecimiento__dependencia_funcional__tipo_gestion__nombre='Estatal', anexo_domicilio__tipo_domicilio__descripcion='Institucional', anexo_domicilio__localidad__id=localidad_id).all().order_by('cue')]
    extensiones = [{'Localidad': ue.get_domicilio_institucional().localidad.nombre, 'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': ue.id, 'CueAnexo': ue.cue, 'Instituto': ue.nombre, 'Gestion': ue.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ue in ExtensionAulica.objects.filter(establecimiento__dependencia_funcional__tipo_gestion__nombre='Estatal', domicilio__tipo_domicilio__descripcion='Institucional', domicilio__localidad__id=localidad_id).all().order_by('cue')]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getPadronCarreras(request):
    from apps.titulos.models import Carrera
    q = [{'IDCarrera': c.id, 'Carrera': c.nombre} for c in Carrera.objects.all().order_by('nombre')]
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")


@require_http_methods(["GET"])
def getCarrerasPorInstituto(request, cueanexo, anio):
    anios_disponibles = ['2013', '2014', '2015', '2016']
    if anio not in anios_disponibles:
        r = json.dumps({'error': u'Año inválido. Debe ser entre ' + anios_disponibles[0] + ' y ' + anios_disponibles[-1]}, ensure_ascii=False)
        return HttpResponse(r, mimetype = "application/javascript")

    from apps.titulos.models import Cohorte, CohorteEstablecimiento, CarreraJurisdiccional, Carrera, CohorteAnexo, CohorteExtensionAulica
    q1 = CohorteEstablecimiento.objects.filter(establecimiento__cue=cueanexo, cohorte__anio=anio)
    q2 = CohorteAnexo.objects.filter(anexo__cue=cueanexo, cohorte__anio=anio)
    q3 = CohorteExtensionAulica.objects.filter(extension_aulica__cue=cueanexo, cohorte__anio=anio)

    q1.distinct().order_by('establecimiento__dependencia_funcional__jurisdiccion__nombre', 'establecimiento__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
    q2.distinct().order_by('anexo__dependencia_funcional__jurisdiccion__nombre', 'anexo__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
    q3.distinct().order_by('extension_aulica__dependencia_funcional__jurisdiccion__nombre', 'extension_aulica__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')

    sedes = [{'Anio': ce.cohorte.anio, 'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ce.get_unidad_educativa().id, 'Instituto': ce.get_unidad_educativa().nombre, 'CueAnexo': ce.get_unidad_educativa().cue, 'IDCarrera': ce.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ce.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ce.get_establecimiento().dependencia_funcional.tipo_gestion.nombre} for ce in q1]
    anexos = [{'Anio': ca.cohorte.anio, 'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ca.get_unidad_educativa().id, 'Instituto': ca.get_unidad_educativa().nombre, 'CueAnexo': ca.get_unidad_educativa().cue, 'IDCarrera': ca.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ca.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ca.get_establecimiento().dependencia_funcional.tipo_gestion.nombre} for ca in q2]
    extensiones = [{'Anio': cea.cohorte.anio, 'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': cea.get_unidad_educativa().id, 'Instituto': cea.get_unidad_educativa().nombre, 'CueAnexo': cea.get_unidad_educativa().cue, 'IDCarrera': cea.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': cea.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': cea.get_establecimiento().dependencia_funcional.tipo_gestion.nombre} for cea in q3]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")



