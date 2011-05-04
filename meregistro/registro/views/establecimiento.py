# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required
from seguridad.models import Usuario, Perfil
from meregistro.registro.models.Establecimiento import Establecimiento
from meregistro.registro.models.Estado import Estado
from meregistro.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from meregistro.registro.forms.EstablecimientoFormFilters import EstablecimientoFormFilters
from meregistro.registro.forms.EstablecimientoForm import EstablecimientoForm
from django.core.paginator import Paginator
from meregistro.registro.helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50

@login_required
def index(request):

	"""
	Búsqueda de establecimientos
	"""
	if request.method == 'GET':
		form_filter = EstablecimientoFormFilters(request.GET)
	else:
		form_filter = EstablecimientoFormFilters()
	q = build_query(form_filter, 1, request)

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
	return my_render(request, 'registro/establecimiento/index.html', {
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


def build_query(filters, page, request):
  """
  Construye el query de búsqueda a partir de los filtros.
  """
  return filters.buildQuery().order_by('nombre').filter(ambito__path__istartswith=request.get_perfil().ambito.path)

@login_required
def create(request):
	"""
	Alta de establecimiento.
	"""
	if request.method == 'POST':
		form = EstablecimientoForm(request.POST)
		if form.is_valid(): # guardar
			establecimiento = form.save()
			estado = Estado.objects.get(nombre = Estado.PENDIENTE)
			establecimiento.registrar_estado(estado)

			MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_CREATE, establecimiento)
			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('establecimientoEdit', args = [establecimiento.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = EstablecimientoForm()

	return my_render(request, 'registro/establecimiento/new.html', {
		'form': form,
		'is_new': True,
	})

@login_required
def edit(request, establecimiento_id):
	"""
	Edición de los datos de un establecimiento.
	"""
	establecimiento = Establecimiento.objects.get(pk = establecimiento_id)
	if request.method == 'POST':
		form = EstablecimientoForm(request.POST, instance = establecimiento)
		if form.is_valid(): # guardar
			establecimiento = form.save()

			MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning','Ocurrió un error actualizando los datos.')
	else:
		form = EstablecimientoForm(instance = establecimiento)

	return my_render(request, 'registro/establecimiento/edit.html', {
		'form': form,
		'establecimiento': establecimiento,
	})

@login_required
def delete(request, establecimiento_id):
	establecimiento = Establecimiento.objects.get(pk = establecimiento_id)
	has_anexos = establecimiento.hasAnexos()
	# TODO: chequear que pertenece al ámbito
	if has_anexos:
		request.set_flash('warning', 'No se puede eliminar el establecimiento porque tiene anexos asociados.')
	elif not establecimiento.isDeletable():
		request.set_flash('warning', 'El establecimiento no se puede eliminar.')
	else:
		establecimiento.delete()
		MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_DELETE, establecimiento)
		request.set_flash('success', 'Registro eliminado correctamente.')
	return HttpResponseRedirect(reverse('establecimiento'))
