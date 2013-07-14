# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Ambito, Rol
from apps.validez_nacional.forms import ValidezNacionalFormFilters, ValidezNacionalForm
from apps.validez_nacional.models import ValidezNacional
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
#from apps.reportes.views.validez_nacional import solicitudes as reporte_solicitudes
#from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50
"""
def __puede_editarse_solicitud(request, solicitud):
	# Sólo se puede editar mientras está en estado Pendiente
	# pero el AdminNacional puede hacerlo en estado Controlado también
	return (solicitud.estado.nombre == EstadoSolicitud.PENDIENTE) or \
		(solicitud.estado.nombre == EstadoSolicitud.CONTROLADO and request.get_perfil().rol.nombre == Rol.ROL_ADMIN_NACIONAL)
"""

@login_required
@credential_required('validez_nacional_validez_index')
def index(request):
	
	if request.method == 'GET':
		form_filter = ValidezNacionalFormFilters(request.GET)
	else:
		form_filter = SolicitudFormFilters()
	q = build_query(form_filter, 1, request)

	"""
	try:
		if request.GET['export'] == '1':
			return reporte_solicitudes(request, q)
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
	return my_render(request, 'validez_nacional/validez/index.html', {
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
	return filters.buildQuery().order_by('titulo_nacional', 'primera_cohorte')


@login_required
@credential_required('validez_nacional_validez_editar')
def edit(request, validez_id):
	validez = ValidezNacional.objects.get(pk=validez_id)
	
	if request.method == 'POST':
		form = ValidezNacionalForm(request.POST, instance=validez)
		if form.is_valid():
			v = form.save()

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = ValidezNacionalForm(instance=validez)
	
	return my_render(request, 'validez_nacional/validez/edit.html', {
		'validez': validez,
		'form': form,
	})
