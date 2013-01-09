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
from django.core.paginator import Paginator


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

	"""
	try:
		if request.GET['export'] == '1':
			return reporte_establecimientos(request, q)
	except KeyError:
		pass
	"""
	
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
		#'export_url': Reporte.build_export_url(request.build_absolute_uri()),
	})


def build_query(filters, page, request):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().filter()




def detalle(request, titulo_id):
	"""
	Detalle del Título
	"""
	titulo = Titulo.objects.get(pk=titulo_id)
	if titulo.unidad_educativa.tipo_unidad_educativa == 'establecimiento':
		ue = Establecimiento.objects.get(cue=titulo.unidad_educativa.cue)
		jurisdiccion = ue.dependencia_funcional.jurisdiccion
	elif titulo.unidad_educativa.tipo_unidad_educativa == 'establecimiento':
		ue = Anexo.objects.get(cue=titulo.unidad_educativa.cue)
		jurisdiccion = ue.establecimiento.dependencia_funcional.jurisdiccion
	else:
		ue = None
		
	return my_render(request, 'consulta_validez/detalle.html', {
		'titulo': titulo,
		'ue': ue,
		'dom': ue.get_domicilio_institucional(),
		'jurisdiccion': jurisdiccion,
	})
