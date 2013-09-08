# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models import Carrera, TituloNacional
from apps.validez_nacional.models import ValidezNacional
from apps.consulta_validez.forms import ConsultaValidezFormFilters
from apps.registro.models import Jurisdiccion, Establecimiento, Anexo
from apps.reportes.views.consulta_validez import consulta_validez as reporte_consulta_validez
from apps.reportes.models import Reporte
from django.core.paginator import Paginator
import simplejson as json
from django.core import serializers
from itertools import chain

ITEMS_PER_PAGE = 50

def index(request):
	"""
	Consulta de títulos
	"""
	if request.method == 'GET':
		form_filter = ConsultaValidezFormFilters(request.GET)
	else:
		form_filter = ConsultaValidezFormFilters()
	
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
	q = filters.buildQuery()
	return q


def detalle(request, validez_nacional_id):
	"""
	Detalle del Título Validado
	"""
	validez_nacional = ValidezNacional.objects.get(pk=validez_nacional_id)		
	ue = validez_nacional.get_unidad_educativa()
	return my_render(request, 'consulta_validez/detalle.html', {
		'validez_nacional': validez_nacional,
		'ue': ue,
	})


def ajax_get_unidades_por_jurisdiccion(request, jurisdiccion_id):
	if int(jurisdiccion_id) > 0:
		sedes = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=jurisdiccion_id).order_by('cue').values_list('id', 'cue', 'nombre')
		anexos = Anexo.objects.filter(establecimiento__dependencia_funcional__jurisdiccion__id=jurisdiccion_id).order_by('cue').values_list('id', 'cue', 'nombre')
	else:
		sedes = Establecimiento.objects.order_by('cue').values_list('id', 'cue', 'nombre')
		anexos = Anexo.objects.order_by('cue').values_list('id', 'cue', 'nombre')
		
	unidades_educativas = [(ue[0], ue[1] + " - " + ue[2]) for ue in list(chain(sedes, anexos))]
	return HttpResponse(json.dumps(unidades_educativas), mimetype='application/json')
	

def ajax_get_unidades_por_tipo_gestion(request, tipo_gestion_id):
	if int(tipo_gestion_id) > 0:
		sedes = Establecimiento.objects.filter(dependencia_funcional__tipo_gestion_id=tipo_gestion_id).order_by('cue').values_list('id', 'cue', 'nombre')
		anexos = Anexo.objects.filter(establecimiento__dependencia_funcional__tipo_gestion_id=tipo_gestion_id).order_by('cue').values_list('id', 'cue', 'nombre')
	else:
		sedes = Establecimiento.objects.order_by('cue').values_list('id', 'cue', 'nombre')
		anexos = Anexo.objects.order_by('cue').values_list('id', 'cue', 'nombre')
		
	unidades_educativas = [(ue[0], ue[1] + " - " + ue[2]) for ue in list(chain(sedes, anexos))]
	return HttpResponse(json.dumps(unidades_educativas), mimetype='application/json')
