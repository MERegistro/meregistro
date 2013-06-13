# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.registro.models import Establecimiento, EstadoEstablecimiento, Anexo, EstadoAnexo
from apps.titulos.models import TituloNacional, EstadoTituloNacional, EstadoNormativaJurisdiccional
from apps.validez_nacional.forms import SolicitudFormFilters, SolicitudDatosBasicosForm, SolicitudNormativasForm,\
	SolicitudCohortesForm, SolicitudControlForm
from apps.validez_nacional.models import EstadoSolicitud, Solicitud
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.validez_nacional import solicitudes as reporte_solicitudes
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50

def __puede_editarse_solicitud(solicitud):
	return solicitud.estado.nombre == EstadoSolicitud.PENDIENTE
	

def __flat_list(list_to_flat):
	"Método para aplanar las listas"
	return [i for j in list_to_flat for i in j]
	

@login_required
@credential_required('validez_nacional_consulta')
def index(request):
	
	if request.method == 'GET':
		form_filter = SolicitudFormFilters(request.GET)
	else:
		form_filter = SolicitudFormFilters()
	q = build_query(form_filter, 1, request)

	try:
		if request.GET['export'] == '1':
			return reporte_solicitudes(request, q)
	except KeyError:
		pass
		
	if request.get_perfil().jurisdiccion():
		q = q.filter(jurisdiccion__id=request.get_perfil().jurisdiccion().id)
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
	return my_render(request, 'validez_nacional/solicitud/index.html', {
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
	return filters.buildQuery().order_by('-estado__nombre', 'titulo_nacional__nombre', 'primera_cohorte')


@login_required
@credential_required('validez_nacional_solicitud')
def create(request):
	try:
		jurisdiccion_id = jurisdiccion_id=request.get_perfil().jurisdiccion().id
	except AttributeError:
		jurisdiccion_id = None
	if request.method == 'POST':
		form = SolicitudDatosBasicosForm(request.POST, jurisdiccion_id=jurisdiccion_id)
		if form.is_valid():
			solicitud = form.save(commit=False)
			solicitud.estado = EstadoSolicitud.objects.get(nombre=EstadoSolicitud.PENDIENTE)
			solicitud.jurisdiccion = request.get_perfil().jurisdiccion()
			solicitud.save()
			
			solicitud.registrar_estado()

			request.set_flash('success', 'Datos guardados correctamente.')

			return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = SolicitudDatosBasicosForm(jurisdiccion_id=jurisdiccion_id)
	# Agrego el filtro por jurisdicción
	return my_render(request, 'validez_nacional/solicitud/new.html', {
		'form': form,
		'form_template': 'validez_nacional/solicitud/form_datos_basicos.html',
		'is_new': True,
		'page_title': 'Título',
		'current_page': 'datos_basicos',
	})


@login_required
@credential_required('validez_nacional_editar_solicitud')
# Editar datos básicos
def edit(request, solicitud_id):
	"""
	Edición de los datos de un título jurisdiccional.
	"""
	solicitud = Solicitud.objects.get(pk=solicitud_id)
	
	if not __puede_editarse_solicitud(solicitud):
		request.set_flash('warning', 'No puede editarse la solicitud.')
		return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
	
	estado_id = solicitud.estado_id
		
	if request.method == 'POST':
		form = SolicitudDatosBasicosForm(request.POST, instance=solicitud, jurisdiccion_id=solicitud.jurisdiccion_id)
		if form.is_valid():
			sol = form.save(commit=False)
			sol.id = solicitud.id
			sol.jurisdiccion_id = solicitud.jurisdiccion_id
			sol.estado_id = solicitud.estado_id
			form.save()

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = SolicitudDatosBasicosForm(instance=solicitud, jurisdiccion_id=solicitud.jurisdiccion_id)
	return my_render(request, 'validez_nacional/solicitud/edit.html', {
		'form': form,
		'solicitud': solicitud,
		'form_template': 'validez_nacional/solicitud/form_datos_basicos.html',
		'is_new': False,
		'page_title': 'Título',
		'current_page': 'datos_basicos',
	})


@login_required
@credential_required('validez_nacional_editar_solicitud')
def editar_normativas(request, solicitud_id):
	"""
	Edición de normativas
	"""
	try:
		solicitud = Solicitud.objects.get(pk=solicitud_id)
	except:
		# Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
		return my_render(request, 'validez_nacional/solicitud/new.html', {
			'solicitud': None,
			'form_template': 'validez_nacional/solicitud/form_normativas.html',
			'page_title': 'Normativas',
			'current_page': 'normativas',
	})

	if not __puede_editarse_solicitud(solicitud):
		request.set_flash('warning', 'No puede editarse la solicitud.')
		return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
		
	if request.method == 'POST':
		form = SolicitudNormativasForm(request.POST, instance=solicitud)
		if form.is_valid():
			normativas = form.save()

			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('solicitudNormativasEdit', args=[solicitud.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = SolicitudNormativasForm(instance=solicitud)

	form.fields['normativas_jurisdiccionales'].queryset = form.fields['normativas_jurisdiccionales'].queryset.filter(jurisdiccion=request.get_perfil().jurisdiccion)

	return my_render(request, 'validez_nacional/solicitud/edit.html', {
		'form': form,
		'solicitud': solicitud,
		'form_template': 'validez_nacional/solicitud/form_normativas.html',
		'is_new': False,
		'page_title': 'Normativas',
		'current_page': 'normativas',
	})


@login_required
@credential_required('validez_nacional_editar_solicitud')
def editar_cohortes(request, solicitud_id):
	"""
	Edición de datos de cohortes
	"""
	try:
		solicitud = Solicitud.objects.get(pk=solicitud_id)
	except:
		# Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
		return my_render(request, 'validez_nacional/solicitud/new.html', {
		'solicitud': None,
		'is_new': True,
		'form_template': 'validez_nacional/solicitud/form_cohortes.html',
		'page_title': 'Cohortes',
		'current_page': 'cohortes',
	})

	if not __puede_editarse_solicitud(solicitud):
		request.set_flash('warning', 'No puede editarse la solicitud.')
		return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
		
	if request.method == 'POST':
		form = SolicitudCohortesForm(request.POST, instance=solicitud)
		if form.is_valid():
			cohorte = form.save()
			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('solicitudCohortesEdit', args=[solicitud.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = SolicitudCohortesForm(instance=solicitud)
	return my_render(request, 'validez_nacional/solicitud/edit.html', {
		'form': form,
		'solicitud': solicitud,
		'form_template': 'validez_nacional/solicitud/form_cohortes.html',
		'is_new': solicitud.primera_cohorte is None and solicitud.ultima_cohorte is None,
		'page_title': 'Cohortes',
		'current_page': 'cohortes',
	})


@login_required
@credential_required('validez_nacional_control')
def control(request, solicitud_id):
	solicitud = Solicitud.objects.get(pk=solicitud_id)
	estado_anterior = solicitud.estado
	
	if request.method == 'POST':
		form = SolicitudControlForm(request.POST, instance=solicitud)
		if form.is_valid():
			sol = form.save()
			if sol.estado != estado_anterior:
				sol.registrar_estado()

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = SolicitudControlForm(instance=solicitud)
	return my_render(request, 'validez_nacional/solicitud/edit.html', {
		'form': form,
		'solicitud': solicitud,
		'form_template': 'validez_nacional/solicitud/form_control.html',
		'is_new': False,
		'page_title': 'Control de Solicitud',
		'current_page': 'control',
	})

@login_required
@credential_required('validez_nacional_editar_solicitud')
def asignar_establecimientos(request, solicitud_id):
	solicitud = Solicitud.objects.get(pk=solicitud_id)

	if not __puede_editarse_solicitud(solicitud):
		request.set_flash('warning', 'No puede editarse la solicitud.')
		return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
	
	"Traigo los ids de los establecimientos actualmente asignados a la solicitud"
	current_establecimientos_ids = __flat_list(solicitud.establecimientos.all().values_list("establecimiento_id"))
	
	q = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path, estado__nombre=EstadoEstablecimiento.REGISTRADO)
	
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
	
	"Procesamiento"
	if request.method == 'POST':
		values_dict = {
			'establecimientos_procesados_ids': [e.id for e in objects], #  Son los establecimientos de la página actual
			'current_establecimientos_ids': current_establecimientos_ids,
			'establecimientos_seleccionados_ids': request.POST.getlist("establecimientos"),
		}
		
		solicitud.save_establecimientos(**values_dict)

		request.set_flash('success', 'Datos actualizados correctamente.')
		# redirigir a edit
		return HttpResponseRedirect(reverse('solicitudAsignarEstablecimientos', args=[solicitud.id]))

	return my_render(request, 'validez_nacional/solicitud/asignar_establecimientos.html', {
		'solicitud': solicitud,
		'current_establecimientos_ids': current_establecimientos_ids,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})
	
	
@login_required
@credential_required('validez_nacional_editar_solicitud')
def asignar_anexos(request, solicitud_id):
	solicitud = Solicitud.objects.get(pk=solicitud_id)

	if not __puede_editarse_solicitud(solicitud):
		request.set_flash('warning', 'No puede editarse la solicitud.')
		return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
	
	"Traigo los ids de los establecimientos actualmente asignados a la solicitud"
	current_anexos_ids = __flat_list(solicitud.anexos.all().values_list("anexo_id"))
	
	q = Anexo.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path, estado__nombre=EstadoAnexo.REGISTRADO)
	
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
	
	"Procesamiento"
	if request.method == 'POST':
		values_dict = {
			'anexos_procesados_ids': [a.id for a in objects], #  Son los establecimientos de la página actual
			'current_anexos_ids': current_anexos_ids,
			'anexos_seleccionados_ids': request.POST.getlist("anexos"),
		}
		
		solicitud.save_anexos(**values_dict)

		request.set_flash('success', 'Datos actualizados correctamente.')
		# redirigir a edit
		return HttpResponseRedirect(reverse('solicitudAsignarAnexos', args=[solicitud.id]))

	return my_render(request, 'validez_nacional/solicitud/asignar_anexos.html', {
		'solicitud': solicitud,
		'current_anexos_ids': current_anexos_ids,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})


@login_required
@credential_required('validez_nacional_eliminar_solicitud')
def delete(request, solicitud_id):
	solicitud = Solicitud.objects.get(pk=solicitud_id)

	if solicitud.is_deletable():
		solicitud.delete()
		request.set_flash('success', 'Registro eliminado correctamente.')
	else:
		request.set_flash('warning', 'El registro no puede ser eliminado.')
	return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
