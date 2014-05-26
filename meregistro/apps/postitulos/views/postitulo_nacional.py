# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.postitulos.models import PostituloNacional, EstadoPostituloNacional
from apps.postitulos.forms import PostituloNacionalFormFilters, PostituloNacionalForm
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.titulo_nacional import titulos_nacionales as reporte_titulos_nacionales
from apps.reportes.models import Reporte

ITEMS_PER_PAGE = 50


@login_required
@credential_required('tit_titulo_nacional_consulta')
def index(request):
	"""
	Búsqueda de titulos
	"""
	if request.method == 'GET':
		form_filter = PostituloNacionalFormFilters(request.GET)
	else:
		form_filter = PostituloNacionalFormFilters()
	q = build_query(form_filter, 1, request)

	try:
		if request.GET['export'] == '1':
			return reporte_titulos_nacionales(request, q)
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
	return my_render(request, 'postitulos/postitulo_nacional/index.html', {
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
	return filters.buildQuery().order_by('nombre')


@login_required
@credential_required('tit_titulo_nacional_alta')
def create(request):
	"""
	Alta de título nacional.
	"""
	if request.method == 'POST':
		form = TituloNacionalForm(request.POST)
		if form.is_valid():
			titulo_nacional = form.save(commit=False)
			titulo_nacional.estado = EstadoTituloNacional.objects.get(nombre=EstadoTituloNacional.VIGENTE)
			titulo_nacional.save()
			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
			titulo_nacional.registrar_estado()

			#MailHelper.notify_by_email(MailHelper.TITULO_CREATE, titulo)
			request.set_flash('success', 'Datos guardados correctamente.')

			# redirigir a edit
			return HttpResponseRedirect(reverse('tituloNacionalEdit', args=[titulo_nacional.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = TituloNacionalForm()

	form.fields['estado'].queryset = EstadoTituloNacional.objects.filter(nombre=EstadoTituloNacional.VIGENTE)
	return my_render(request, 'titulos/titulo_nacional/new.html', {
		'form': form,
		'is_new': True,
	})


@login_required
@credential_required('tit_titulo_nacional_modificar')
def edit(request, titulo_nacional_id):
	"""
	Edición de los datos de un título nacional.
	"""
	titulo_nacional = TituloNacional.objects.get(pk=titulo_nacional_id)
	estado_actual_id = titulo_nacional.estado.id

	if request.method == 'POST':
		form = TituloNacionalForm(request.POST, instance=titulo_nacional, initial={'estado': estado_actual_id})
		if form.is_valid():
			titulo_nacional = form.save(commit=False)

			"Cambiar el estado?"
			if int(request.POST['estado']) is not estado_actual_id:
				titulo_nacional.estado = EstadoTituloNacional.objects.get(pk=request.POST['estado'])
				titulo_nacional.save()
				titulo_nacional.registrar_estado()
			else:
				# Guardar directamente
				titulo_nacional.save()

			form.save_m2m()  # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method

			#MailHelper.notify_by_email(MailHelper.TITULO_UPDATE, titulo)
			request.set_flash('success', 'Datos actualizados correctamente.')
		else:
			request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
	else:
		form = TituloNacionalForm(instance=titulo_nacional, initial={'estado': estado_actual_id})

	return my_render(request, 'titulos/titulo_nacional/edit.html', {
		'form': form,
		'is_new': False,
	})




@login_required
@credential_required('tit_titulo_nacional_baja')
def delete(request, titulo_nacional_id):
	titulo_nacional = TituloNacional.objects.get(pk=titulo_nacional_id)

	if titulo_nacional.is_deletable():
		titulo_nacional.delete()
		request.set_flash('success', 'Registro eliminado correctamente.')
	else:
		request.set_flash('warning', 'El registro no puede ser eliminado.')
	return HttpResponseRedirect(reverse('tituloNacional'))
