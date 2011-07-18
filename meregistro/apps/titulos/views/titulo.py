# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import Titulo, EstadoTitulo
from apps.titulos.forms import TituloFormFilters, TituloForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50

@login_required
@credential_required('tit_titulo_consulta')
def index(request):
    """
    Búsqueda de titulos
    """
    if request.method == 'GET':
        form_filter = TituloFormFilters(request.GET)
    else:
        form_filter = TituloFormFilters()
    q = build_query(form_filter, 1, request)

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        form_filter.fields["jurisdiccion"].queryset = Jurisdiccion.objects.filter(dependenciafuncional__jurisdiccion__id = jurisdiccion.id)
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
    return my_render(request, 'titulos/titulo/index.html', {
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
    return filters.buildQuery().order_by('nombre')

@login_required
@credential_required('tit_titulo_alta')
def create(request):
    """
    Alta de título.
    """
    if request.method == 'POST':
        form = TituloForm(request.POST)
        if form.is_valid():
            titulo = form.save()
            estado = EstadoTitulo.objects.get(nombre = EstadoTitulo.VIGENTE)
            titulo.registrar_estado(estado)

            MailHelper.notify_by_email(MailHelper.TITULO_CREATE, titulo)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloEdit', args = [titulo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloForm()

    return my_render(request, 'titulos/titulo/new.html', {
        'form': form,
        'is_new': True,
    })


@login_required
@credential_required('tit_titulo_modificar')
def edit(request, titulo_id):
    """
    Edición de los datos de un título.
    """
    titulo = Titulo.objects.get(pk = titulo_id)
    estado_actual = titulo.getEstadoActual()

    if estado_actual is None:
        estado_actual_id = None
    else:
        estado_actual_id = estado_actual.id

    if request.method == 'POST':
        form = TituloForm(request.POST, instance = titulo, initial = {'estado': estado_actual_id})
        if form.is_valid():
            titulo = form.save()

            "Cambiar el estado?"
            if int(request.POST['estado']) is not estado_actual_id:
                estado = EstadoTitulo.objects.get(pk = int(request.POST['estado']))
                titulo.registrar_estado(estado)

            MailHelper.notify_by_email(MailHelper.TITULO_UPDATE, titulo)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = TituloForm(instance = titulo, initial = {'estado': estado_actual_id})

    return my_render(request, 'titulos/titulo/edit.html', {
        'form': form,
        'is_new': False,
    })

@login_required
@credential_required('tit_titulo_eliminar')
def eliminar(request, titulo_id):
    """
    Baja de un título
    --- mientras no sea referido por un título jurisdiccional ---
    """
    titulo = Titulo.objects.get(pk = titulo_id)
    request.set_flash('warning', 'Está seguro de eliminar el título? Esta opración no puede deshacerse.')
    if request.method == 'POST':
        if int(request.POST['titulo_id']) is not int(titulo_id):
            raise Exception('Error en la consulta!')
        titulo.delete()
        request.set_flash('success', 'El título fue dado de baja correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('titulosHome'))
    return my_render(request, 'titulos/titulo/eliminar.html', {
        'titulo_id': titulo.id,
    })
