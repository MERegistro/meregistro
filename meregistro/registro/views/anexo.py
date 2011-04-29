# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required
from seguridad.models import Usuario, Perfil
from registro.models import Establecimiento, Anexo, AnexoEstado
from registro.forms import AnexoFormFilters, AnexoForm
from django.core.paginator import Paginator
import datetime

ITEMS_PER_PAGE = 50

@login_required
def index(request):
	"""
	Búsqueda de anexos
	"""
	if request.method == 'GET':
		form_filter = AnexoFormFilters(request.GET)
	else:
		form_filter = AnexoFormFilters()
	q = build_query(form_filter, 1)

	paginator = Paginator(q, ITEMS_PER_PAGE)

	try:
		page_number = int(request.GET['page']) # page es un int?
	except (KeyError, ValueError):
		page_number = 1
	# chequear los límites
	if page_number < 1:
		page_number = 1
	elif page_number > paginator.num_pages:
		page_number = paginator.num_pages

	page = paginator.page(page_number)
	objects = page.object_list
	return my_render(request, 'registro/anexo/index.html', {
		'form_filters': form_filter,
		'objects': objects,
		'show_paginator': paginator.num_pages > 1,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'page': page_number,
		'pages': paginator.num_pages,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})

def build_query(filters, page):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	return filters.buildQuery().order_by('establecimiento__nombre', 'cue')

@login_required
def create(request):
	"""
	Alta de anexo.
	"""
	if request.method == 'POST':
		form = AnexoForm(request.POST)
		if form.is_valid(): # guardar
			anexo = form.save(commit = False)
			estado = AnexoEstado()
			request.set_flash('success', 'Datos guardados correctamente.')

			# redirigir a edit
			return HttpResponseRedirect(reverse('anexoEdit', args=[anexo.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = AnexoForm()

	return my_render(request, 'registro/anexo/new.html', {
		'form': form,
		'is_new': True,
	})

@login_required
def edit(request, anexo_id):
	"""
	Edición de los datos de un anexo.
	"""
	anexo = Anexo.objects.get(pk = anexo_id)
	if request.method == 'POST':
		form = AnexoForm(request.POST, instance = anexo)
		if form.is_valid(): # guardar
			anexo = form.save()
			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning','Ocurrió un error actualizando los datos.')
	else:
		form = AnexoForm(instance = anexo)

	return my_render(request, 'registro/anexo/edit.html', {
		'form': form,
		'anexo': anexo,
	})
