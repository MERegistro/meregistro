# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import Titulo, EstadoTitulo, TituloOrientacion, EstadoTituloOrientacion
from apps.titulos.forms import TituloFormFilters, TituloForm, TituloOrientacionFormFilters, TituloOrientacionForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50

def build_query(filters, page, request):
    "Construye el query de búsqueda a partir de los filtros."
    return filters.buildQuery().order_by('nombre', 'titulo__nombre')

@login_required
@credential_required('tit_orientacion_consulta')
def index(request):
    """
    Búsqueda de orientaciones
    """
    if request.method == 'GET':
        form_filter = TituloOrientacionFormFilters(request.GET)
    else:
        form_filter = TituloOrientacionFormFilters()
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
    return my_render(request, 'titulos/orientacion/index.html', {
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

@login_required
@credential_required('tit_orientacion_consulta')
def orientaciones_por_titulo(request, titulo_id):
    "Búsqueda de orientaciones por título"
    titulo = Titulo.objects.get(pk = titulo_id)
    q = TituloOrientacion.objects.filter(titulo__id = titulo.id)
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
    return my_render(request, 'titulos/orientacion/orientaciones_por_titulo.html', {
        'titulo': titulo,
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

@login_required
@credential_required('tit_orientacion_alta')
def create(request, titulo_id = None):
    "Agregar orientación al título actual o crearla eligiendo el mismo"
    if titulo_id is not None:
        titulo = Titulo.objects.get(pk = titulo_id)
    else:
        titulo = None

    if request.method == 'POST':
        form = TituloOrientacionForm(request.POST)
        if form.is_valid():
            orientacion = form.save()
            estado = EstadoTituloOrientacion.objects.get(nombre = EstadoTituloOrientacion.VIGENTE)
            orientacion.registrar_estado(estado)

            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('orientacionesPorTitulo', args = [orientacion.titulo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloOrientacionForm()

    if titulo:
        form.fields["titulo"].queryset = Titulo.objects.filter(id = titulo.id)
        form.fields["titulo"].empty_label = None

    return my_render(request, 'titulos/orientacion/new.html', {
        'form': form,
        'titulo': titulo,
        'is_new': True,
    })

@login_required
@credential_required('tit_orientacion_modificar')
def edit(request, orientacion_id):
    " Edición de los datos de una orientación "
    orientacion = TituloOrientacion.objects.get(pk = orientacion_id)

    estado_actual = orientacion.getEstadoActual()
    if estado_actual is None:
        estado_actual_id = None
    else:
        estado_actual_id = estado_actual.id

    if request.method == 'POST':
        form = TituloOrientacionForm(request.POST, instance = orientacion, initial = {'estado': estado_actual_id})
        if form.is_valid():
            titulo = form.save()

            "Cambiar el estado?"
            if int(request.POST['estado']) is not estado_actual_id:
                estado = EstadoTituloOrientacion.objects.get(pk = int(request.POST['estado']))
                orientacion.registrar_estado(estado)

            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('orientacionesPorTitulo', args = [orientacion.titulo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = TituloOrientacionForm(instance = orientacion, initial = {'estado': estado_actual_id})

    form.fields["titulo"].queryset = Titulo.objects.filter(id = orientacion.titulo.id)
    form.fields["titulo"].empty_label = None

    return my_render(request, 'titulos/orientacion/edit.html', {
        'form': form,
        'titulo': orientacion.titulo,
        'is_new': False,
    })

"""
@login_required
@credential_required('tit_titulo_eliminar')
def eliminar(request, titulo_id):
    "Baja de un título    --- mientras no sea referido por un título jurisdiccional ---"
    titulo = Titulo.objects.get(pk = titulo_id)
    request.set_flash('warning', 'Está seguro de eliminar el título? Esta opración no puede deshacerse.')
    if request.method == 'POST':
        if int(request.POST['titulo_id']) is not int(titulo_id):
            raise Exception('Error en la consulta!')
        titulo.delete()
        request.set_flash('success', 'El título fue dado de baja correctamente.')
        "Redirecciono para evitar el reenvío del form"
        return HttpResponseRedirect(reverse('titulosHome'))
    return my_render(request, 'titulos/titulo/eliminar.html', {
        'titulo_id': titulo.id,
    })
"""