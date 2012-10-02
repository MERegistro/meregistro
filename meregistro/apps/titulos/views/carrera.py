# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models import Carrera, EstadoCarrera, TituloNacional
from apps.titulos.forms import CarreraFormFilters, CarreraForm, CarreraAsignarTitulosFormFilters
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.carrera import carreras as reporte_carreras
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


@login_required
@credential_required('tit_carrera_consulta')
def index(request):
	if request.method == 'GET':
		form_filter = CarreraFormFilters(request.GET)
	else:
		form_filter = CarreraFormFilters()
	q = build_query(form_filter, 1)

	try:
		if request.GET['export'] == '1':
			return reporte_carreras(request, q)
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

	return my_render(request, 'titulos/carrera/index.html', {
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
		form = CarreraForm(request.POST)
		if form.is_valid():
			carrera = form.save(commit=False)
			carrera.estado = EstadoCarrera.objects.get(nombre=EstadoCarrera.VIGENTE)
			carrera.save()
			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
			carrera.registrar_estado()

			request.set_flash('success', 'Datos guardados correctamente.')

			# redirigir a edit
			return HttpResponseRedirect(reverse('carreraEdit', args=[carrera.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CarreraForm()
	
	form.fields['estado'].queryset = EstadoCarrera.objects.filter(nombre=EstadoCarrera.VIGENTE)
	return my_render(request, 'titulos/carrera/new.html', {
		'form': form,
		'is_new': True,
	})


@login_required
@credential_required('tit_carrera_modificar')
def edit(request, carrera_id):
	carrera = Carrera.objects.get(pk=carrera_id)
	if request.method == 'POST':
		form = CarreraForm(request.POST, instance=carrera)
		if form.is_valid():
			carrera = form.save()
			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = CarreraForm(instance=carrera)

	return my_render(request, 'titulos/carrera/edit.html', {
		'form': form,
		'carrera': carrera,
	})

def edit(request, carrera_id):
	"""
	Edición de los datos de una carrera.
	"""
	carrera = Carrera.objects.get(pk=carrera_id)

	estado_actual_id = carrera.estado.id

	if request.method == 'POST':
		form = CarreraForm(request.POST, instance=carrera, initial={'estado': estado_actual_id})
		if form.is_valid():
			carrera = form.save(commit=False)

			"Cambiar el estado?"
			if int(request.POST['estado']) is not estado_actual_id:
				carrera.estado = EstadoCarrera.objects.get(pk=request.POST['estado'])
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
		form = CarreraForm(instance=carrera, initial={'estado': estado_actual_id})

	return my_render(request, 'titulos/carrera/edit.html', {
		'form': form,
		'carrera': carrera,
	})


@login_required
@credential_required('tit_carrera_baja')
def delete(request, carrera_id):
	carrera = Carrera.objects.get(pk=carrera_id)

	carrera.delete()
	request.set_flash('success', 'Registro eliminado correctamente.')

	return HttpResponseRedirect(reverse('carrera'))
	
	
def __flat_list(list_to_flat):
	"Método para aplanar las listas"
	return [i for j in list_to_flat for i in j]

def build_query_asignar_titulos(filters):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().order_by('nombre')


@credential_required('tit_carrera_asignar_titulos')
@login_required
def titulos(request, carrera_id):
	carrera = Carrera.objects.get(pk=carrera_id)
	
	current_titulos_ids = __flat_list(carrera.titulos_asignados.all().values_list("id"))

	if request.method == 'GET':
		form_filter = CarreraAsignarTitulosFormFilters(request.GET)
	else:
		form_filter = CarreraAsignarTitulosFormFilters()
				
		# POST, guardo los datos
		post_ids = request.POST.getlist('titulos')
		
		"Borrar los que se des-chequean, pero sólo si la carrera no es jurisdiccional"
		if not carrera.carrera_jurisdiccional():
			for titulo_id in current_titulos_ids:
				if str(titulo_id) not in post_ids: # Si no está en los nuevos ids, borrarlo
					carrera.titulos_asignados.remove(str(titulo_id))
		
		"Vuelvo a calcular"
		current_titulos_ids = __flat_list(carrera.titulos_asignados.all().values_list("id"))
		"Agregar los nuevos"
		for titulo_id in post_ids:
			"Si no está entre los actuales"
			if int(titulo_id) not in current_titulos_ids:
				# Lo agrego
				carrera.titulos_asignados.add(int(titulo_id))

		request.set_flash('success', 'Datos actualizados correctamente.')
		return HttpResponseRedirect(reverse('carreraTitulos', args=[carrera.id]))
		
	objects = build_query_asignar_titulos(form_filter)
	
	return my_render(request, 'titulos/carrera/titulos.html', {
		'carrera': carrera,
		'form_filters': form_filter,
		'objects': objects,
		'current_titulos_ids': current_titulos_ids,
	})
	
