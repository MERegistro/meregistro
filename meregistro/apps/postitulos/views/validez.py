# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Ambito, Rol
from apps.postitulos.forms import ValidezNacionalFormFilters, ValidezNacionalForm
from apps.postitulos.models import ValidezNacional
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
#from apps.reportes.views.validez_nacional import solicitudes as reporte_solicitudes
#from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


@login_required
@credential_required('validez_nacional_validez_index')
def index(request):

	jur = request.get_perfil().jurisdiccion()

	if request.method == 'GET':
		form_filter = ValidezNacionalFormFilters(request.GET, jurisdiccion=jur)
	else:
		form_filter = ValidezNacionalFormFilters(jurisdiccion=jur)
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
	return my_render(request, 'postitulos/validez/index.html', {
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
	return filters.buildQuery().order_by('postitulo_nacional', 'primera_cohorte')


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
	
	return my_render(request, 'postitulos/validez/edit.html', {
		'validez': validez,
		'form': form,
	})


@login_required
@credential_required('validez_nacional_validez_editar')
def eliminar(request, validez_nacional_id):
	"""
	No sólo deberá eliminarse el registro de la tabla validez_nacional_validez_nacional, 
	sino que también deberá eliminarse la asignación que había hacia ese CUE de la 
	Solicitud de Validez Nacional correspondiente (en la tabla validez_nacional_solicitud_establecimientos
	o en la tabla validez_nacional_solicitud_anexos según sea un registro de una Sede o un Anexo), 
	como si el registro que se está eliminando nunca hubiera sido parte de la solicitud original.
	"""
	validez_nacional = ValidezNacional.objects.get(pk=validez_nacional_id)
	
	if request.method == 'POST':
		if int(request.POST['validez_nacional_id']) != int(validez_nacional_id):
			raise Exception('Error en la consulta!')
		validez_nacional.delete()
		request.set_flash('success', 'El registro de Validez Nacional fue eliminado correctamente.')
		""" Redirecciono para evitar el reenvío del form """
		return HttpResponseRedirect(reverse('postituloValidezNacionalIndex'))
	return my_render(request, 'postitulos/validez/eliminar.html', {
		'validez_nacional_id': validez_nacional.id,
	})
