# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.oferta_nacional.forms import OfertaNacionalFormFilters
from apps.registro.models import Jurisdiccion, Establecimiento
from apps.titulos.models import Carrera
from apps.reportes.views.oferta_nacional import oferta_nacional as reporte_oferta_nacional
from apps.reportes.models import Reporte
from django.core.paginator import Paginator
import simplejson as json
from django.core import serializers


ITEMS_PER_PAGE = 50
ANIOS_DISPONIBLES = [2013]


def index(request, anio):
    if int(anio) not in ANIOS_DISPONIBLES:
	    raise Exception('Año no disponible para consulta')
    """
    Consulta de títulos
    """
    if request.method == 'GET':
        form_filter = OfertaNacionalFormFilters(request.GET)
    else:
        form_filter = OfertaNacionalFormFilters()

    q = build_query(form_filter, 1, request)

    try:
        if request.GET['export'] == '1':
            return reporte_oferta_nacional(request, q, anio)
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
    return my_render(request, 'oferta_nacional/index.html', {
		'anio': anio,
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
    q = q.order_by('establecimiento__dependencia_funcional__jurisdiccion__nombre', 'establecimiento__cue', 'cohorte__carrera_jurisdiccional__carrera__nombre')
    return q


def ajax_get_establecimientos_por_jurisdiccion(request, jurisdiccion_id):
    if int(jurisdiccion_id) > 0:
        establecimientos = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=jurisdiccion_id)
    else:
        establecimientos = Establecimiento.objects.all()
    
    establecimientos.order_by('nombre')
    json_establecimientos = serializers.serialize("json", establecimientos)
    return HttpResponse(json_establecimientos, mimetype = "application/javascript")


def ajax_get_carreras_por_jurisdiccion(request, jurisdiccion_id):
    carreras = Carrera.objects.filter(carrerajurisdiccional__jurisdiccion__id=jurisdiccion_id)
    json_carreras = serializers.serialize("json", carreras)
    return HttpResponse(json_carreras, mimetype = "application/javascript")


def ajax_get_carreras_por_establecimiento(request, establecimiento_id):
    carreras = Carrera.objects.filter(carrerajurisdiccional__cohortes__establecimientos__id=establecimiento_id)
    json_carreras = serializers.serialize("json", carreras)
    return HttpResponse(json_carreras, mimetype = "application/javascript")

