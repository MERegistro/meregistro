# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import CarreraJurisdiccional, Cohorte, CohorteEstablecimiento, EstadoCarreraJurisdiccional, EstadoCohorteEstablecimiento, \
	CohorteAnexo, EstadoCohorteAnexo, CohorteExtensionAulica, \
	EstadoCohorteExtensionAulica, CarreraJurisdiccionalCohorte
from apps.titulos.forms import CarreraJurisdiccionalCohorteFormFilters, CohorteForm, CohorteAsignarEstablecimientosFormFilters, \
	CohorteAsignarAnexosFormFilters, CohorteAsignarExtensionesAulicasFormFilters
from apps.registro.models import Jurisdiccion, Establecimiento
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime
from apps.reportes.views.cohorte_jurisdiccional import cohortes_jurisdiccionales as reporte_cohortes_jurisdiccionales
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


def build_query(filters, page, request):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	if filters.jur:
		q = filters.buildQuery().order_by('carrera__nombre')
	else:
		q = filters.buildQuery().order_by('jurisdiccion__nombre', 'carrera__nombre')
	return q

@login_required
@credential_required('tit_cohorte_consulta')
def index(request):
	"""
	Búsqueda de titulos
	"""
	jur = request.get_perfil().jurisdiccion()
	if request.method == 'GET':
		form_filter = CarreraJurisdiccionalCohorteFormFilters(request.GET, jurisdiccion=jur)
	else:
		form_filter = CarreraJurisdiccionalCohorteFormFilters(jurisdiccion=jur)
	q = build_query(form_filter, 1, request)

	try:
		if request.GET['export'] == '1':
			return reporte_cohortes_jurisdiccionales(request, q)
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
	
	
	return my_render(request, 'titulos/cohorte/index.html', {
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


@login_required
#@credential_required('tit_cohorte_alta')
def create(request, carrera_jurisdiccional_id):
	"""
	Alta de cohorte
	"""
	carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)

	if request.method == 'POST':
		form = CohorteForm(request.POST)
		if form.is_valid():
			cohorte = form.save()

			# redirigir a edit
			request.set_flash('success', 'Datos guardados correctamente.')
			return HttpResponseRedirect(reverse('cohortesPorCarreraJurisdiccional', args=[carrera_jurisdiccional.id]))

		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CohorteForm()

	choices = [('', '-------')]
	"""
	try:
		for cohorte in carrera_jurisdiccional.datos_cohorte.all():
			choices += [(i, i) for i in range(cohorte.primera_cohorte_solicitada, cohorte.ultima_cohorte_solicitada + 1)]
	except CarreraJurisdiccionalCohorte.DoesNotExist:
		pass
	form.fields["anio"].choices = choices
	"""
	form.fields["carrera_jurisdiccional"].initial = carrera_jurisdiccional.id

	return my_render(request, 'titulos/cohorte/new.html', {
		'form': form,
		'carrera_jurisdiccional': carrera_jurisdiccional,
		'is_new': True,
	})


@login_required
#@credential_required('tit_cohorte_modificar')
# Editar datos básicos
def edit(request, cohorte_id):
	"""
	Edición de los datos de una cohorte.
	"""
	cohorte = Cohorte.objects.get(pk=cohorte_id)

	if request.method == 'POST':
		form = CohorteForm(request.POST, instance=cohorte)
		if form.is_valid():

			cohorte = form.save()

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = CohorteForm(instance=cohorte)

	carrera_jurisdiccional = cohorte.carrera_jurisdiccional
	"""
	choices = []
	for a_cohorte in carrera_jurisdiccional.datos_cohorte.all():
		choices += [(i, i) for i in range(a_cohorte.primera_cohorte_solicitada, a_cohorte.ultima_cohorte_solicitada + 1)]
	form.fields["anio"].choices = choices
	"""
	asignada_establecimiento = cohorte.asignada_establecimiento()
	if asignada_establecimiento:
		form.fields["anio"].choices = [(cohorte.anio, cohorte.anio)]
	
	# No se puede modificar la carrera ni el año
	form.fields["carrera_jurisdiccional"].queryset = CarreraJurisdiccional.objects.filter(id=cohorte.carrera_jurisdiccional_id)
	form.fields["carrera_jurisdiccional"].empty_label = None

	return my_render(request, 'titulos/cohorte/edit.html', {
		'form': form,
		'cohorte': cohorte,
		'carrera_jurisdiccional': cohorte.carrera_jurisdiccional,
		'asignada_establecimiento': asignada_establecimiento,
		'is_new': False,
	})


@login_required
@credential_required('tit_cohorte_consulta')
def cohortes_por_carrera_jurisdiccional(request, carrera_jurisdiccional_id):
	"Cohortes por título"
	carrera_jurisdiccional = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	q = Cohorte.objects.filter(carrera_jurisdiccional__id=carrera_jurisdiccional.id)
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
	return my_render(request, 'titulos/cohorte/cohortes_por_carrera_jurisdiccional.html', {
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
@credential_required('tit_cohorte_asignar')
def asignar_establecimientos(request, cohorte_id):
	"""
	Asignar cohorte a establecimientos
	"""
	cohorte = Cohorte.objects.get(pk=cohorte_id)
	"Traigo los ids de los establecimientos actualmente asignados a la cohorte"
	current_establecimientos_ids = __flat_list(CohorteEstablecimiento.objects.filter(cohorte=cohorte).values_list("establecimiento_id"))
	
	"Búsqueda de establecimientos"
	if request.method == 'GET':
		form_filters = CohorteAsignarEstablecimientosFormFilters(request.GET)
	else:
		form_filters = CohorteAsignarEstablecimientosFormFilters()		

	jurisdiccion = request.get_perfil().jurisdiccion()
	
	form_filters.fields["dependencia_funcional"].queryset = form_filters.fields["dependencia_funcional"].queryset.filter(jurisdiccion=jurisdiccion)
	
	q = build_asignar_establecimientos_query(form_filters, request)
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
		estado = EstadoCohorteEstablecimiento.objects.get(nombre=EstadoCohorteEstablecimiento.ASIGNADA)
		values_dict = {
			'establecimientos_procesados_ids': [e.id for e in objects], #  Son los establecimientos de la página actual
			'current_establecimientos_ids': current_establecimientos_ids,
			'establecimientos_seleccionados_ids': request.POST.getlist("establecimientos"),
			'estado': estado,
		}
		cohorte.save_establecimientos(**values_dict)

		request.set_flash('success', 'Datos actualizados correctamente.')
		# redirigir a edit
		return HttpResponseRedirect(reverse('cohorteAsignarEstablecimientos', args=[cohorte.id]))


	return my_render(request, 'titulos/cohorte/asignar_establecimientos.html', {
		'cohorte': cohorte,
		'current_establecimientos_ids': current_establecimientos_ids,
		'form_filters': form_filters,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})


def build_asignar_establecimientos_query(filters, request):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().filter(ambito__path__istartswith=request.get_perfil().ambito.path)


@login_required
@credential_required('tit_cohorte_asignar')
def asignar_anexos(request, cohorte_id):
	"""
	Asignar cohorte a anexos
	"""
	cohorte = Cohorte.objects.get(pk=cohorte_id)
	"Traigo los ids de los anexos actualmente asignados a la cohorte"
	current_anexos_ids = __flat_list(CohorteAnexo.objects.filter(cohorte=cohorte).values_list("anexo_id"))
	
	"Búsqueda de anexos"
	if request.method == 'GET':
		form_filters = CohorteAsignarAnexosFormFilters(request.GET)
	else:
		form_filters = CohorteAsignarAnexosFormFilters()		

	jurisdiccion = request.get_perfil().jurisdiccion()
	
	form_filters.fields["dependencia_funcional"].queryset = form_filters.fields["dependencia_funcional"].queryset.filter(jurisdiccion=jurisdiccion)
	
	q = build_asignar_anexos_query(form_filters, request)
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
		estado = EstadoCohorteAnexo.objects.get(nombre=EstadoCohorteAnexo.ASIGNADA)
		values_dict = {
			'anexos_procesados_ids': [a.id for a in objects], #  Son los anexos de la página actual
			'current_anexos_ids': current_anexos_ids,
			'anexos_seleccionados_ids': request.POST.getlist("anexos"),
			'estado': estado,
		}
		cohorte.save_anexos(**values_dict)

		request.set_flash('success', 'Datos actualizados correctamente.')
		# redirigir a edit
		return HttpResponseRedirect(reverse('cohorteAsignarAnexos', args=[cohorte.id]))


	return my_render(request, 'titulos/cohorte/asignar_anexos.html', {
		'cohorte': cohorte,
		'current_anexos_ids': current_anexos_ids,
		'form_filters': form_filters,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})


def build_asignar_anexos_query(filters, request):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().filter(ambito__path__istartswith=request.get_perfil().ambito.path).order_by('nombre')


@login_required
@credential_required('tit_cohorte_asignar')
def asignar_extensiones_aulicas(request, cohorte_id):
	"""
	Asignar cohorte a extensiones áulicas
	"""
	cohorte = Cohorte.objects.get(pk=cohorte_id)
	"Traigo los ids de las extensiones áulicas actualmente asignados a la cohorte"
	current_extensiones_aulicas_ids = __flat_list(CohorteExtensionAulica.objects.filter(cohorte=cohorte).values_list("extension_aulica_id"))
	
	"Búsqueda de extensiones áulicas"
	if request.method == 'GET':
		form_filters = CohorteAsignarExtensionesAulicasFormFilters(request.GET)
	else:
		form_filters = CohorteAsignarExtensionesAulicasFormFilters()		

	jurisdiccion = request.get_perfil().jurisdiccion()
	
	form_filters.fields["dependencia_funcional"].queryset = form_filters.fields["dependencia_funcional"].queryset.filter(jurisdiccion=jurisdiccion)
	
	q = build_asignar_extensiones_aulicas_query(form_filters, request)
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
		estado = EstadoCohorteExtensionAulica.objects.get(nombre=EstadoCohorteExtensionAulica.ASIGNADA)
		values_dict = {
			'extensiones_aulicas_procesadas_ids': [e.id for e in objects], #  Son las extensiones de la página actual
			'current_extensiones_aulicas_ids': current_extensiones_aulicas_ids,
			'extensiones_aulicas_seleccionadas_ids': request.POST.getlist("extensiones_aulicas"),
			'estado': estado,
		}
		cohorte.save_extensiones_aulicas(**values_dict)

		request.set_flash('success', 'Datos actualizados correctamente.')
		# redirigir a edit
		return HttpResponseRedirect(reverse('cohorteAsignarExtensionesAulicas', args=[cohorte.id]))


	return my_render(request, 'titulos/cohorte/asignar_extensiones_aulicas.html', {
		'cohorte': cohorte,
		'current_extensiones_aulicas_ids': current_extensiones_aulicas_ids,
		'form_filters': form_filters,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})


def build_asignar_extensiones_aulicas_query(filters, request):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().filter(establecimiento__ambito__path__istartswith=request.get_perfil().ambito.path)


@login_required
@credential_required('tit_cohorte_eliminar')
def eliminar(request, cohorte_id):
	"""
	Baja de una cohorte
	--- mientras no estén asignadas a un establecimiento ---
	"""
	cohorte = Cohorte.objects.get(pk=cohorte_id)
	asignada_establecimiento = cohorte.asignada_establecimiento()

	if asignada_establecimiento:
		request.set_flash('warning', 'La cohorte no puede darse de baja porque tiene establecimientos asignados.')
	else:
		request.set_flash('warning', 'Está seguro de eliminar la cohorte? Esta operación no puede deshacerse.')

	if request.method == 'POST':
		if int(request.POST['cohorte_id']) is not int(cohorte.id):
			raise Exception('Error en la consulta!')

		cohorte.delete()
		request.set_flash('success', 'La cohorte fue eliminada correctamente.')
		""" Redirecciono para evitar el reenvío del form """
		return HttpResponseRedirect(reverse('cohorte'))

	return my_render(request, 'titulos/cohorte/eliminar.html', {
		'cohorte': cohorte,
		'cohorte_id': cohorte.id,
		'asignada_establecimiento': asignada_establecimiento,
	})


def __flat_list(list_to_flat):
	"Método para aplanar las listas"
	return [i for j in list_to_flat for i in j]


@login_required
#@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, oid):
	o = Cohorte.objects.get(pk=oid)
	o.revisado_jurisdiccion = True
	o.save()
	request.set_flash('success', 'Registro revisado.')
	return HttpResponseRedirect(reverse('cohortesPorTitulo', args=[o.carrera_jurisdiccional_id]))
