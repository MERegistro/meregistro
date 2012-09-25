# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models import NormativaNacional, EstadoNormativaNacional
from apps.titulos.forms import NormativaNacionalFormFilters, NormativaNacionalForm
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 50


@login_required
@credential_required('tit_normativa_nacional_consulta')
def index(request):
	if request.method == 'GET':
		form_filter = NormativaNacionalFormFilters(request.GET)
	else:
		form_filter = NormativaNacionalFormFilters()
	q = build_query(form_filter, 1)

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

	return my_render(request, 'titulos/normativa_nacional/index.html', {
		'form_filters': form_filter,
		'objects': objects,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1,
	})


def build_query(filters, page):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().order_by('numero')


@login_required
@credential_required('tit_normativa_nacional_alta')
def create(request):
	import datetime
	if request.method == 'POST':
		form = NormativaNacionalForm(request.POST)
		if form.is_valid():
			normativa_nacional = form.save(commit=False)
			normativa_nacional.estado = EstadoNormativaNacional.objects.get(nombre=EstadoNormativaNacional.VIGENTE)
			normativa_nacional.save()
			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
			normativa_nacional.registrar_estado()

			request.set_flash('success', 'Datos guardados correctamente.')

			# redirigir a edit
			return HttpResponseRedirect(reverse('normativaNacionalEdit', args=[normativa_nacional.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = NormativaNacionalForm()
	
	form.fields['estado'].queryset = EstadoNormativaNacional.objects.filter(nombre=EstadoNormativaNacional.VIGENTE)
	return my_render(request, 'titulos/normativa_nacional/new.html', {
		'form': form,
		'is_new': True,
	})


@login_required
@credential_required('tit_normativa_nacional_modificar')
def edit(request, normativa_nacional_id):
	normativa_nacional = NormativaNacional.objects.get(pk=normativa_nacional_id)
	if request.method == 'POST':
		form = NormativaNacionalForm(request.POST, instance=normativa_nacional)
		if form.is_valid():
			normativa_nacional = form.save()
			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = NormativaNacionalForm(instance=normativa_nacional)

	return my_render(request, 'titulos/normativa_nacional/edit.html', {
		'form': form,
		'normativa_nacional': normativa_nacional,
	})

def edit(request, normativa_nacional_id):
	"""
	Edición de los datos de una normativa nacional.
	"""
	normativa_nacional = NormativaNacional.objects.get(pk=normativa_nacional_id)

	estado_actual_id = normativa_nacional.estado.id

	if request.method == 'POST':
		form = NormativaNacionalForm(request.POST, instance=normativa_nacional, initial={'estado': estado_actual_id})
		if form.is_valid():
			normativa_nacional = form.save(commit=False)

			"Cambiar el estado?"
			if int(request.POST['estado']) is not estado_actual_id:
				normativa_nacional.estado = EstadoNormativaNacional.objects.get(pk=request.POST['estado'])
				normativa_nacional.save()
				normativa_nacional.registrar_estado()
			else:
				# Guardar directamente
				normativa_nacional.save()

			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method

			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = NormativaNacionalForm(instance=normativa_nacional, initial={'estado': estado_actual_id})

	return my_render(request, 'titulos/normativa_nacional/edit.html', {
		'form': form,
		'normativa_nacional': normativa_nacional,
	})


@login_required
@credential_required('tit_normativa_nacional_baja')
def delete(request, normativa_nacional_id):
	normativa_nacional = NormativaNacional.objects.get(pk=normativa_nacional_id)

	if not normativa_nacional.asociada_titulo():
		normativa_nacional.delete()
		request.set_flash('success', 'Registro eliminado correctamente.')
	else:
		request.set_flash('warning', 'El registro no puede ser eliminado porque tiene títulos asociados.')
	return HttpResponseRedirect(reverse('normativaNacional'))
