# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.postitulos.models import CarreraPostitulo, EstadoCarreraPostitulo, PostituloNacional
from apps.postitulos.forms import CarreraPostituloFormFilters, CarreraPostituloForm, CarreraAsignarPostitulosFormFilters
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
#from apps.reportes.views.carrera import carreras as reporte_carreras
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


@login_required
@credential_required('tit_carrera_consulta')
def index(request):
	if request.method == 'GET':
		form_filter = CarreraPostituloFormFilters(request.GET)
	else:
		form_filter = CarreraPostituloFormFilters()
	q = build_query(form_filter, 1)

	try:
		if request.GET['export'] == '1':
			return reporte_carreras_postitulos(request, q)
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

	return my_render(request, 'postitulos/carrera/index.html', {
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


def build_query(filters, page):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().order_by('nombre')


@login_required
@credential_required('tit_carrera_alta')
def create(request):
	import datetime
	if request.method == 'POST':
		form = CarreraPostituloForm(request.POST)
		if form.is_valid():
			carrera = form.save(commit=False)
			carrera.estado = EstadoCarreraPostitulo.objects.get(nombre=EstadoCarreraPostitulo.VIGENTE)
			carrera.save()
			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
			carrera.registrar_estado()

			request.set_flash('success', 'Datos guardados correctamente.')

			# redirigir a edit
			return HttpResponseRedirect(reverse('carreraPostituloEdit', args=[carrera.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CarreraPostituloForm()
	
	form.fields['estado'].queryset = EstadoCarreraPostitulo.objects.filter(nombre=EstadoCarreraPostitulo.VIGENTE)
	return my_render(request, 'postitulos/carrera/new.html', {
		'form': form,
		'is_new': True,
	})

@login_required
@credential_required('tit_carrera_alta')
def edit(request, carrera_id):
	"""
	Edición de los datos de una carrera.
	"""
	carrera = CarreraPostitulo.objects.get(pk=carrera_id)

	estado_actual_id = carrera.estado.id

	if request.method == 'POST':
		form = CarreraPostituloForm(request.POST, instance=carrera, initial={'estado': estado_actual_id})
		if form.is_valid():
			carrera = form.save(commit=False)

			"Cambiar el estado?"
			if int(request.POST['estado']) is not estado_actual_id:
				carrera.estado = EstadoCarreraPostitulo.objects.get(pk=request.POST['estado'])
				carrera.save()
				carrera.registrar_estado()
			else:
				# Guardar directamente
				carrera.save()

			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = CarreraPostituloForm(instance=carrera, initial={'estado': estado_actual_id})

	return my_render(request, 'postitulos/carrera/edit.html', {
		'form': form,
		'carrera': carrera,
	})


@login_required
@credential_required('tit_carrera_baja')
def delete(request, carrera_id):
	carrera = CarreraPostitulo.objects.get(pk=carrera_id)

	carrera.delete()
	request.set_flash('success', 'Registro eliminado correctamente.')

	return HttpResponseRedirect(reverse('carreraPostitulo'))
	
	
def __flat_list(list_to_flat):
	"Método para aplanar las listas"
	return [i for j in list_to_flat for i in j]

def build_query_asignar_postitulos(filters):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().order_by('nombre')


@credential_required('tit_carrera_asignar_titulos')
@login_required
def postitulos(request, carrera_id):
	carrera = CarreraPostitulo.objects.get(pk=carrera_id)
	
	current_postitulos_ids = __flat_list(carrera.postitulos_asignados.all().values_list("id"))
	if request.method == 'GET':
		form_filter = CarreraAsignarPostitulosFormFilters(request.GET)
	else:
		form_filter = CarreraAsignarPostitulosFormFilters()
				
		# POST, guardo los datos
		post_ids = request.POST.getlist('postitulos')
		
		"Borrar los que se des-chequean, pero sólo si la carrera no es jurisdiccional"
		#if not carrera.carrera_jurisdiccional():
		for postitulo_id in current_postitulos_ids:
			if str(postitulo_id) not in post_ids: # Si no está en los nuevos ids, borrarlo
				carrera.postitulos_asignados.remove(str(postitulo_id))
		
		"Vuelvo a calcular"
		current_postitulos_ids = __flat_list(carrera.postitulos_asignados.all().values_list("id"))
		"Agregar los nuevos"
		for postitulo_id in post_ids:
			"Si no está entre los actuales"
			if int(postitulo_id) not in current_postitulos_ids:
				# Lo agrego
				carrera.postitulos_asignados.add(int(postitulo_id))

		request.set_flash('success', 'Datos actualizados correctamente.')
		return HttpResponseRedirect(reverse('carreraPostitulos', args=[carrera.id]))
		
	objects = build_query_asignar_postitulos(form_filter)
	
	return my_render(request, 'postitulos/carrera/postitulos.html', {
		'carrera': carrera,
		'form_filters': form_filter,
		'objects': objects,
		'current_postitulos_ids': current_postitulos_ids,
	})
	
