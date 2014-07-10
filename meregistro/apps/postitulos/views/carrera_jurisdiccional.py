# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.postitulos.models import EstadoCarreraPostituloJurisdiccional, CarreraPostituloJurisdiccional #, Titulo, EstadoTitulo, TituloOrientacion, \
	#EstadoTituloOrientacion, EstadoNormativaJurisdiccional, \
	#CarreraJurisdiccionalCohorte
from apps.postitulos.forms import CarreraPostituloJurisdiccionalFormFilters, CarreraPostituloJurisdiccionalDatosBasicosForm #, CarreraPoJurisdiccionalForm, \
	#CarreraJurisdiccionalOrientacionesForm, \
	#CarreraJurisdiccionalDuracionForm, CarreraJurisdiccionalNormativasForm, CarreraJurisdiccionalSolicitarCohortesForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50


def build_query(filters, page, request):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().filter(jurisdiccion=request.get_perfil().jurisdiccion()).order_by('carrera_postitulo__nombre')


@login_required
@credential_required('tit_carrera_jurisdiccional_consulta')
def index(request):
	"""
	Búsqueda de titulos
	"""
	if request.method == 'GET':
		form_filter = CarreraPostituloJurisdiccionalFormFilters(request.GET)
	else:
		form_filter = CarreraPostituloJurisdiccionalFormFilters()
	q = build_query(form_filter, 1, request)
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
	
	return my_render(request, 'postitulos/carrera_jurisdiccional/index.html', {
		'form_filters': form_filter,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})


@login_required
@credential_required('tit_carrera_jurisdiccional_alta')
def create(request):
	"""
	Alta de título jurisdiccional.
	"""
	if request.method == 'POST':
		form = CarreraPostituloJurisdiccionalDatosBasicosForm(request.POST, jurisdiccion_id=request.get_perfil().jurisdiccion().id)
		if form.is_valid():
			carrera_jurisdiccional = form.save(commit=False)
			carrera_jurisdiccional.estado = EstadoCarreraPostituloJurisdiccional.objects.get(nombre=EstadoCarreraPostituloJurisdiccional.REGISTRADO)
			carrera_jurisdiccional.jurisdiccion = request.get_perfil().jurisdiccion()
			carrera_jurisdiccional.save()
			#form.save_m2m() # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
			carrera_jurisdiccional.registrar_estado()

			request.set_flash('success', 'Datos guardados correctamente.')

			# redirigir a edit
			return HttpResponseRedirect(reverse('carreraPostituloJurisdiccionalEdit', args=[carrera_jurisdiccional.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CarreraPostituloJurisdiccionalDatosBasicosForm(jurisdiccion_id=request.get_perfil().jurisdiccion().id)
	# Agrego el filtro por jurisdicción
	return my_render(request, 'postitulos/carrera_jurisdiccional/new.html', {
		'form': form,
		'form_template': 'postitulos/carrera_jurisdiccional/form_datos_basicos.html',
		'is_new': True,
		'page_title': 'Datos básicos',
		'current_page': 'datos_basicos',
	})


@login_required
@credential_required('tit_carrera_jurisdiccional_modificar')
# Editar datos básicos
def edit(request, carrera_postitulo_jurisdiccional_id):
	"""
	Edición de los datos de un título jurisdiccional.
	"""
	carrera_postitulo_jurisdiccional = CarreraPostituloJurisdiccional.objects.get(pk=carrera_postitulo_jurisdiccional_id)
	postitulo_anterior_id = int(carrera_postitulo_jurisdiccional.carrera_postitulo_id)

	if request.method == 'POST':
		form = CarreraPostituloJurisdiccionalDatosBasicosForm(request.POST, instance=carrera_postitulo_jurisdiccional, jurisdiccion_id=request.get_perfil().jurisdiccion().id)
		if form.is_valid():
			carrera_postitulo_jurisdiccional = form.save()

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = CarreraPostituloJurisdiccionalDatosBasicosForm(instance=carrera_postitulo_jurisdiccional, jurisdiccion_id=request.get_perfil().jurisdiccion().id)

	return my_render(request, 'postitulos/carrera_jurisdiccional/edit.html', {
		'form': form,
		'carrera_jurisdiccional': carrera_postitulo_jurisdiccional,
		'form_template': 'postitulos/carrera_jurisdiccional/form_datos_basicos.html',
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
			return HttpResponseRedirect(reverse('carreraPostituloJurisdiccionalOrientacionesEdit', args=[carrera_jurisdiccional.id]))
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
			return HttpResponseRedirect(reverse('carreraPostituloJurisdiccionalNormativasEdit', args=[carrera_jurisdiccional.id]))
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
@credential_required('non_existent_credential')
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
			return HttpResponseRedirect(reverse('carreraPostituloJurisdiccionalCohortesEdit', args=[carrera_jurisdiccional.id]))
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
@credential_required('tit_carrera_jurisdiccional_eliminar')
def eliminar(request, carrera_jurisdiccional_id):
	"""
	Baja de un título
	--- mientras no sea referido por un título jurisdiccional ---
	"""
	carrera = CarreraJurisdiccional.objects.get(pk=carrera_jurisdiccional_id)
	tiene_cohortes_generadas = carrera.tiene_cohortes_generadas()
	if request.method == 'POST':
		if int(request.POST['carrera_jurisdiccional_id']) != int(carrera_jurisdiccional_id):
			raise Exception('Error en la consulta!')
		if tiene_cohortes_generadas:
			raise Exception('No puede eliminarse la carrera ya que tiene cohortes generadas')
		carrera.delete()
		request.set_flash('success', 'La carrera jurisdiccional fue dada de baja correctamente.')
		""" Redirecciono para evitar el reenvío del form """
		return HttpResponseRedirect(reverse('carreraPostituloJurisdiccional'))
	return my_render(request, 'titulos/carrera_jurisdiccional/eliminar.html', {
		'carrera_jurisdiccional_id': carrera.id,
		'tiene_cohortes_generadas': tiene_cohortes_generadas,
	})


@login_required
#@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, oid):
	o = CarreraJurisdiccional.objects.get(pk=oid)
	o.revisado_jurisdiccion = True
	o.estado = EstadoCarreraJurisdiccional.objects.get(nombre=EstadoCarreraJurisdiccional.CONTROLADO)
	o.registrar_estado()
	request.set_flash('success', 'Registro revisado.')
	return HttpResponseRedirect(reverse('carreraPostituloJurisdiccional'))
