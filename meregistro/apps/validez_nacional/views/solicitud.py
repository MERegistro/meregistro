# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import TituloNacional, EstadoTituloNacional
from apps.validez_nacional.forms import SolicitudFormFilters, SolicitudDatosBasicosForm
from apps.validez_nacional.models import EstadoSolicitud
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.validez_nacional import solicitudes as reporte_solicitudes
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


@login_required
@credential_required('validez_nacional_solicitud')
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
		q.filter(jurisdiccion=request.get_perfil().jurisdiccion())
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

			# redirigir a edit
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
#@credential_required('tit_carrera_jurisdiccional_modificar')
# Editar datos básicos
def edit(request, carrera_jurisdiccional_id):
	"""
	Edición de los datos de un título jurisdiccional.
	"""
	carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	titulo_anterior_id = int(carrera_jurisdiccional.carrera_id)

	if request.method == 'POST':
		form = CarreraJurisdiccionalDatosBasicosForm(request.POST, instance=carrera_jurisdiccional, jurisdiccion_id=request.get_perfil().jurisdiccion().id)
		if form.is_valid():

			# Cambió el título? Borrar las orientaciones
			cambio_titulo = titulo_anterior_id is not int(request.POST['carrera'])
			if cambio_titulo:
				carrera_jurisdiccional.eliminar_orientaciones()

			carrera_jurisdiccional = form.save()

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = CarreraJurisdiccionalDatosBasicosForm(instance=carrera_jurisdiccional, jurisdiccion_id=request.get_perfil().jurisdiccion().id)

	return my_render(request, 'titulos/carrera_jurisdiccional/edit.html', {
		'form': form,
		'carrera_jurisdiccional': carrera_jurisdiccional,
		'form_template': 'titulos/carrera_jurisdiccional/form_datos_basicos.html',
		'is_new': False,
		'page_title': 'Datos básicos',
		'current_page': 'datos_basicos',
	})


@login_required
#@credential_required('tit_carrera_jurisdiccional_alta')
#@credential_required('tit_carrera_jurisdiccional_modificar')
def editar_orientaciones(request, carrera_jurisdiccional_id):
	"""
	Edición de orientaciones del título jurisdiccional.
	"""
	try:
		carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	except:
		# Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
		return my_render(request, 'titulos/carrera_jurisdiccional/new.html', {
		'carrera_jurisdiccional': None,
		'form_template': 'titulos/carrera_jurisdiccional/form_orientaciones.html',
		'page_title': 'Orientaciones',
		'current_page': 'orientaciones',
	})

	if request.method == 'POST':
		form = CarreraJurisdiccionalOrientacionesForm(request.POST, instance=carrera_jurisdiccional)
		if form.is_valid():
			orientaciones = form.save()

			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('carreraJurisdiccionalOrientacionesEdit', args=[carrera_jurisdiccional.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CarreraJurisdiccionalOrientacionesForm(instance=carrera_jurisdiccional)

	form.fields['orientaciones'].queryset = form.fields['orientaciones'].queryset.filter(titulo=carrera_jurisdiccional.titulo, estado__nombre=EstadoTituloOrientacion.VIGENTE)

	return my_render(request, 'titulos/carrera_jurisdiccional/edit.html', {
		'form': form,
		'carrera_jurisdiccional': carrera_jurisdiccional,
		'form_template': 'titulos/carrera_jurisdiccional/form_orientaciones.html',
		'is_new': False,
		'page_title': 'Orientaciones',
		'current_page': 'orientaciones',
	})


@login_required
#@credential_required('tit_carrera_jurisdiccional_alta')
#@credential_required('tit_carrera_jurisdiccional_modificar')
def editar_normativas(request, carrera_jurisdiccional_id):
	"""
	Edición de normativas del título jurisdiccional.
	"""
	try:
		carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	except:
		# Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
		return my_render(request, 'titulos/carrera_jurisdiccional/new.html', {
		'carrera_jurisdiccional': None,
		'form_template': 'titulos/carrera_jurisdiccional/form_normativas.html',
		'page_title': 'Normativas',
		'current_page': 'normativas',
	})

	if request.method == 'POST':
		form = CarreraJurisdiccionalNormativasForm(request.POST, instance=carrera_jurisdiccional)
		if form.is_valid():
			normativas = form.save()

			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('carreraJurisdiccionalNormativasEdit', args=[carrera_jurisdiccional.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CarreraJurisdiccionalNormativasForm(instance=carrera_jurisdiccional)

	form.fields['normativas'].queryset = form.fields['normativas'].queryset.filter(jurisdiccion=request.get_perfil().jurisdiccion, estado__nombre=EstadoNormativaJurisdiccional.VIGENTE)

	return my_render(request, 'titulos/carrera_jurisdiccional/edit.html', {
		'form': form,
		'carrera_jurisdiccional': carrera_jurisdiccional,
		'form_template': 'titulos/carrera_jurisdiccional/form_normativas.html',
		'is_new': False,
		'page_title': 'Normativas',
		'current_page': 'normativas',
	})


@login_required
#@credential_required('tit_carrera_jurisdiccional_alta')
#@credential_required('tit_carrera_jurisdiccional_modificar')
def editar_cohortes(request, carrera_jurisdiccional_id):
	"""
	Edición de datos de cohortes del título jurisdiccional.
	"""
	try:
		carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	except:
		# Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
		return my_render(request, 'titulos/carrera_jurisdiccional/new.html', {
		'carrera_jurisdiccional': None,
		'form_template': 'titulos/carrera_jurisdiccional/form_cohortes.html',
		'page_title': 'Datos de cohortes',
		'current_page': 'cohortes',
	})

	try:
		cohorte = CarreraJurisdiccionalCohorte.objects.get(carrera_jurisdiccional=carrera_jurisdiccional)
	except:
		cohorte = CarreraJurisdiccionalCohorte(carrera_jurisdiccional=carrera_jurisdiccional)

	if request.method == 'POST':
		form = CarreraJurisdiccionalSolicitarCohortesForm(request.POST, instance=cohorte)
		if form.is_valid():
			cohorte = form.save()
			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('carreraJurisdiccionalCohortesEdit', args=[carrera_jurisdiccional.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CarreraJurisdiccionalSolicitarCohortesForm(instance=cohorte)
		
	try:
		if carrera_jurisdiccional.datos_cohorte.get().id is None:
			is_new = True
		else: 
			is_new = False
	except CarreraJurisdiccionalCohorte.DoesNotExist:
		is_new = True
		
		
	return my_render(request, 'titulos/carrera_jurisdiccional/edit.html', {
		'form': form,
		'carrera_jurisdiccional': carrera_jurisdiccional,
		'form_template': 'titulos/carrera_jurisdiccional/form_cohortes.html',
		'is_new': is_new,
		'page_title': 'Datos de cohortes',
		'current_page': 'cohortes',
	})


@login_required
#@credential_required('tit_carrera_jurisdiccional_consulta')
def orientaciones_por_titulo(request, carrera_jurisdiccional_id):
	"Búsqueda de orientaciones por título jurisdiccional"
	carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	q = TituloOrientacion.objects.filter(titulo__id=carrera_jurisdiccional.titulo_id)
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
	return my_render(request, 'titulos/carrera_jurisdiccional/orientaciones_por_titulo.html', {
		#'form_filters': form_filter,
		'carrera_jurisdiccional': carrera_jurisdiccional,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})


@login_required
#@credential_required('tit_carrera_jurisdiccional_eliminar')
def eliminar(request, carrera_jurisdiccional_id):
	"""
	Baja de un título
	--- mientras no sea referido por un título jurisdiccional ---
	"""
	carrera = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	request.set_flash('warning', 'Está seguro de eliminar la carrera jurisdiccional? Esta operación no puede deshacerse.')
	if request.method == 'POST':
		if int(request.POST['carrera_jurisdiccional_id']) is not int(carrera_jurisdiccional_id):
			raise Exception('Error en la consulta!')
		carrera.delete()
		request.set_flash('success', 'La carrera jurisdiccional fue dada de baja correctamente.')
		""" Redirecciono para evitar el reenvío del form """
		return HttpResponseRedirect(reverse('carreraJurisdiccional'))
	return my_render(request, 'titulos/carrera_jurisdiccional/eliminar.html', {
		'carrera_jurisdiccional_id': carrera.id,
	})


@login_required
#@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, oid):
	o = CarreraJurisdiccional.objects.get(pk=oid)
	o.revisado_jurisdiccion = True
	o.estado = EstadoCarreraJurisdiccional.objects.get(nombre=EstadoCarreraJurisdiccional.CONTROLADO)
	o.registrar_estado()
	request.set_flash('success', 'Registro revisado.')
	return HttpResponseRedirect(reverse('carreraJurisdiccional'))
