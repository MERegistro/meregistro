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

    from django.db import connection
    cursor = connection.cursor()
    sql = '''
SELECT
    'SEDE' AS "tipo_ue",
    est.id AS "id_establecimiento",
    est.cue AS "cueanexo",
    est.nombre AS "instituto",
    tg.nombre AS "tipo_gestion",
    carrera.id AS "id_carrera",
    carrera.nombre AS "carrera",
    c.anio AS "anio"
FROM titulos_cohortes_establecimientos ce
INNER JOIN titulos_cohorte c ON ce.cohorte_id = c.id
INNER JOIN registro_establecimiento est ON ce.establecimiento_id = est.id
INNER JOIN registro_dependencia_funcional df ON est.dependencia_funcional_id = df.id
INNER JOIN registro_tipo_gestion tg ON df.tipo_gestion_id = tg.id
INNER JOIN titulos_carrera_jurisdiccional cj ON c.carrera_jurisdiccional_id = cj.id
INNER JOIN titulos_carrera carrera ON cj.carrera_id = carrera.id
WHERE c.anio = %s

UNION ALL

SELECT 
    'ANEXO' AS "tipo_ue",
    a.id AS "id_establecimiento",
    a.cue AS "cueanexo",
    a.nombre AS "instituto",
    tg.nombre AS "tipo_gestion",
    carrera.id AS "id_carrera",
    carrera.nombre AS "carrera",
    c.anio AS "anio"
FROM titulos_cohortes_anexos ca
INNER JOIN titulos_cohorte c ON ca.cohorte_id = c.id
INNER JOIN registro_anexo a ON ca.anexo_id = a.id
INNER JOIN registro_establecimiento est ON a.establecimiento_id = est.id
INNER JOIN registro_dependencia_funcional df ON est.dependencia_funcional_id = df.id
INNER JOIN registro_tipo_gestion tg ON df.tipo_gestion_id = tg.id
INNER JOIN titulos_carrera_jurisdiccional cj ON c.carrera_jurisdiccional_id = cj.id
INNER JOIN titulos_carrera carrera ON cj.carrera_id = carrera.id
WHERE c.anio = %s

UNION ALL

SELECT 
    'EXTENSIONAULICA' AS "tipo_ue",
    ea.id AS "id_establecimiento",
    ea.cue AS "cueanexo",
    ea.nombre AS "instituto",
    tg.nombre AS "tipo_gestion",
    carrera.id AS "id_carrera",
    carrera.nombre AS "carrera",
    c.anio AS "anio"
FROM titulos_cohortes_extensiones_aulicas cea
INNER JOIN titulos_cohorte c ON cea.cohorte_id = c.id
INNER JOIN registro_extension_aulica ea ON cea.extension_aulica_id = ea.id
INNER JOIN registro_establecimiento est ON ea.establecimiento_id = est.id
INNER JOIN registro_dependencia_funcional df ON est.dependencia_funcional_id = df.id
INNER JOIN registro_tipo_gestion tg ON df.tipo_gestion_id = tg.id
INNER JOIN titulos_carrera_jurisdiccional cj ON c.carrera_jurisdiccional_id = cj.id
INNER JOIN titulos_carrera carrera ON cj.carrera_id = carrera.id
WHERE c.anio = %s

ORDER BY cueanexo;
    '''
    cursor.execute(sql, [anio, anio, anio])

    res = [{'Anio': res[7], 'TipoUnidadEducativa': res[0], 'IDInstituto': res[1], 'Instituto': res[3], 'CueAnexo': res[2], 'IDCarrera': res[5], 'Carrera': res[6], 'Gestion': res[4]} for res in cursor.fetchall()]
    
    '''
    from apps.titulos.models import Cohorte, CohorteEstablecimiento, CarreraJurisdiccional, Carrera, CohorteAnexo, CohorteExtensionAulica
    q1 = CohorteEstablecimiento.objects.filter(cohorte__anio=anio)
    q2 = CohorteAnexo.objects.filter(cohorte__anio=anio)
    q3 = CohorteExtensionAulica.objects.filter(cohorte__anio=anio)

    q1.distinct().order_by('establecimiento__cue',)
    q2.distinct().order_by('anexo__cue')
    q3.distinct().order_by('extension_aulica__cue')

    sedes = [{'Anio': ce.cohorte.anio, 'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ce.establecimiento.id, 'Instituto': ce.establecimiento.nombre, 'CueAnexo': ce.establecimiento.cue, 'IDCarrera': ce.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ce.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ce.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ce in q1]
    anexos = [{'Anio': ca.cohorte.anio, 'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ca.anexo.id, 'Instituto': ca.anexo.nombre, 'CueAnexo': ca.anexo.cue, 'IDCarrera': ca.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ca.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ca.anexo.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ca in q2]
    extensiones = [{'Anio': cea.cohorte.anio, 'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': cea.extension_aulica.id, 'Instituto': cea.extension_aulica.nombre, 'CueAnexo': cea.extension_aulica.cue, 'IDCarrera': cea.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': cea.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': cea.extension_aulica.establecimiento.dependencia_funcional.tipo_gestion.nombre} for cea in q3]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    '''


    j = json.dumps(res, ensure_ascii=False, indent=2)
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

    q1.distinct().order_by('establecimiento__cue',)
    q2.distinct().order_by('anexo__cue')
    q3.distinct().order_by('extension_aulica__cue')

    sedes = [{'Anio': ce.cohorte.anio, 'TipoUnidadEducativa': 'SEDE', 'IDInstituto': ce.establecimiento.id, 'Instituto': ce.establecimiento.nombre, 'CueAnexo': ce.establecimiento.cue, 'IDCarrera': ce.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ce.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ce.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ce in q1]
    anexos = [{'Anio': ca.cohorte.anio, 'TipoUnidadEducativa': 'ANEXO', 'IDInstituto': ca.anexo.id, 'Instituto': ca.anexo.nombre, 'CueAnexo': ca.anexo.cue, 'IDCarrera': ca.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': ca.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': ca.anexo.establecimiento.dependencia_funcional.tipo_gestion.nombre} for ca in q2]
    extensiones = [{'Anio': cea.cohorte.anio, 'TipoUnidadEducativa': 'EXTENSIONAULICA', 'IDInstituto': cea.extension_aulica.id, 'Instituto': cea.extension_aulica.nombre, 'CueAnexo': cea.extension_aulica.cue, 'IDCarrera': cea.cohorte.carrera_jurisdiccional.carrera.id, 'Carrera': cea.cohorte.carrera_jurisdiccional.carrera.nombre, 'Gestion': cea.extension_aulica.establecimiento.dependencia_funcional.tipo_gestion.nombre} for cea in q3]

    import itertools
    q = list(itertools.chain(sedes, anexos, extensiones))
    
    j = json.dumps(q, ensure_ascii=False, indent=2)
    return HttpResponse(j, mimetype = "application/javascript")



