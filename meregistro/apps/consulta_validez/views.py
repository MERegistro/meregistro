# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.consulta_validez.models import UnidadEducativa, Titulo
from apps.consulta_validez.forms import ConsultaValidezFormFilters
from apps.registro.models import Jurisdiccion, Establecimiento, Anexo
from apps.reportes.views.consulta_validez import consulta_validez as reporte_consulta_validez
from apps.reportes.models import Reporte
from django.core.paginator import Paginator
import simplejson as json
from django.core import serializers


ITEMS_PER_PAGE = 50

def ajax_get_carreras(request):
    json_data = json.dumps(choices_carrera(request.GET))
    return HttpResponse(json_data, mimetype = "application/javascript")


def ajax_get_titulos(request):
    json_data = json.dumps(choices_titulo(request.GET))
    return HttpResponse(json_data, mimetype = "application/javascript")


def build_choices_sql(sql, params=[]):
    from django.db import connection, transaction
    cursor = connection.cursor()

    # Data modifying operation - commit required
    cursor.execute(sql, params)
    
    choices = [('', '---------')]
    for c in cursor:
        choices.append((c[0], c[1]))
    return choices

def choices_carrera(filters):
    params = []
    query_carrera = "SELECT DISTINCT t.carrera, t.carrera FROM consulta_validez_titulo t"
    query_carrera += " INNER JOIN consulta_validez_unidadeducativa ue ON t.unidad_educativa_id = ue.id"
    query_carrera += " WHERE 1=1" 
    if filters.has_key('jurisdiccion') and filters['jurisdiccion'] != '':
        query_carrera += " AND ue.jurisdiccion_id = %s"
        params.append(filters['jurisdiccion'])
    if filters.has_key('unidad_educativa') and filters['unidad_educativa'] != '':
        query_carrera += " AND ue.id = %s"
        params.append(filters['unidad_educativa'])
    query_carrera += " ORDER BY carrera"
    return build_choices_sql(query_carrera, params)


def choices_titulo(filters):
    params = []
    query_carrera = "SELECT DISTINCT denominacion, denominacion FROM consulta_validez_titulo t"
    query_carrera += " INNER JOIN consulta_validez_unidadeducativa ue ON t.unidad_educativa_id = ue.id"
    query_carrera += " WHERE 1=1" 
    if filters.has_key('jurisdiccion') and filters['jurisdiccion'] != '':
        query_carrera += " AND ue.jurisdiccion_id = %s"
        params.append(filters['jurisdiccion'])
    if filters.has_key('unidad_educativa') and filters['unidad_educativa'] != '':
        query_carrera += " AND ue.id = %s"
        params.append(filters['unidad_educativa'])
    if filters.has_key('carrera') and filters['carrera'] != '':
        query_carrera += " AND t.carrera = %s"
        params.append(filters['carrera'])
    query_carrera += " ORDER BY denominacion"
    return build_choices_sql(query_carrera, params)




def index(request):

    """
    Consulta de títulos
    """
    if request.method == 'GET':
        form_filter = ConsultaValidezFormFilters(request.GET)
    else:
        form_filter = ConsultaValidezFormFilters()

    form_filter.fields["carrera"].choices = choices_carrera(request.GET)
    form_filter.fields["titulo"].choices = choices_titulo(request.GET)
    if request.GET.has_key('jurisdiccion') and request.GET['jurisdiccion'] != '':
        form_filter.fields['unidad_educativa'].queryset = \
        form_filter.fields['unidad_educativa'].queryset.filter(jurisdiccion=int(request.GET['jurisdiccion']))
    q = build_query(form_filter, 1, request)

    try:
        if request.GET['export'] == '1':
            return reporte_consulta_validez(request, q)
    except KeyError:
        pass

    
    paginator = Paginator(q, ITEMS_PER_PAGE)

    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    # chequear los límites
    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages
        
    page = paginator.page(page_number)
    objects = page.object_list
    return my_render(request, 'consulta_validez/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'export_url': Reporte.build_export_url(request.build_absolute_uri()),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    q = filters.buildQuery().filter()
    q = q.order_by('unidad_educativa__jurisdiccion__nombre', 'unidad_educativa__cue', 'carrera', 'denominacion', 'primera')
    return q

def detalle(request, titulo_id):
    """
    Detalle del Título
    """
    titulo = Titulo.objects.get(pk=titulo_id)
    if titulo.unidad_educativa.tipo_unidad_educativa == 'establecimiento':
        ue = Establecimiento.objects.get(cue=titulo.unidad_educativa.cue)
        jurisdiccion = ue.dependencia_funcional.jurisdiccion
        dom = ue.get_domicilio_institucional()
    elif titulo.unidad_educativa.tipo_unidad_educativa == 'anexo':
        ue = Anexo.objects.get(cue=titulo.unidad_educativa.cue)
        jurisdiccion = ue.establecimiento.dependencia_funcional.jurisdiccion
        dom = ue.get_domicilio_institucional()
    else:
        ue = None
        dom = None
        jurisdiccion = None
        
        
    return my_render(request, 'consulta_validez/detalle.html', {
        'titulo': titulo,
        'ue': ue,
        'dom': dom,
        'jurisdiccion': jurisdiccion,
    })


def ajax_get_unidades_por_jurisdiccion(request, jurisdiccion_id):
    if int(jurisdiccion_id) > 0:
        unidades_educativas = UnidadEducativa.objects.filter(jurisdiccion__id=jurisdiccion_id)
    else:
        unidades_educativas = UnidadEducativa.objects.all()
    
    unidades_educativas.order_by('nombre')
    json_unidades_educativas = serializers.serialize("json", unidades_educativas)
    print json_unidades_educativas
    return HttpResponse(json_unidades_educativas, mimetype = "application/javascript")


def ajax_get_carreras_por_jurisdiccion(request, jurisdiccion_id):
    carreras = choices_carrera(request.GET)
    json_carreras = json.dump(carreras)
    return HttpResponse(json_carreras, mimetype = "application/javascript")


def ajax_get_titulos_por_jurisdiccion(request, jurisdiccion_id):
    if int(jurisdiccion_id) > 0:
        titulos = Titulo.objects.filter(unidad_educativa__jurisdiccion__id=jurisdiccion_id)
    else:
        titulos = Titulo.objects.all()
    
    titulos.order_by('denominacion').distinct('denominacion').values_list('denominacion')
    json_titulos = serializers.serialize("json", titulos)
    return HttpResponse(json_titulos, mimetype = "application/javascript")


def ajax_get_carreras_por_ue(request, ue_id):
    if int(ue_id) > 0:
        carreras = Titulo.objects.filter(unidad_educativa__id=ue_id)
    else:
        carreras = Titulo.objects.all()
    
    carreras.order_by('carrera').distinct('carrera').values_list('carrera')
    json_carreras = serializers.serialize("json", carreras)
    return HttpResponse(json_carreras, mimetype = "application/javascript")


def ajax_get_titulos_por_ue(request, ue_id):
    if int(ue_id) > 0:
        titulos = Titulo.objects.filter(unidad_educativa__id=ue_id)
    else:
        titulos = Titulo.objects.all()
    
    titulos.order_by('denominacion').distinct('denominacion').values_list('denominacion')
    json_titulos = serializers.serialize("json", titulos)
    return HttpResponse(json_titulos, mimetype = "application/javascript")


def ajax_get_titulos_por_carrera(request, carrera_id):
    if int(carrera_id) > 0:
        titulos = Titulo.objects.filter(carrera=Titulo.objects.get(pk=carrera_id).carrera)
    else:
        titulos = Titulo.objects.all()
    
    titulos.order_by('denominacion').distinct('denominacion').values_list('denominacion')
    json_titulos = serializers.serialize("json", titulos)
    return HttpResponse(json_titulos, mimetype = "application/javascript")
