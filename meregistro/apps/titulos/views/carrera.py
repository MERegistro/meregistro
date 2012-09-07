# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.titulos.models import Carrera
from apps.titulos.forms import CarreraFormFilters, CarreraForm
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50


@login_required
@credential_required('tit_carrera_consulta')
def index(request):
    if request.method == 'GET':
        form_filter = CarreraFormFilters(request.GET)
    else:
        form_filter = CarreraFormFilters()
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

    return my_render(request, 'titulos/carrera/index.html', {
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
    return filters.buildQuery().order_by('nombre')


@login_required
@credential_required('tit_carrera_alta')
def create(request):
    if request.method == 'POST':
        form = CarreraForm(request.POST)
        if form.is_valid():
            carrera = form.save(commit=True)

            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('carreraEdit', args=[carrera.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CarreraForm()
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


@login_required
@credential_required('tit_carrera_baja')
def delete(request, carrera_id):
    carrera = Carrera.objects.get(pk=carrera_id)

    carrera.delete()
    request.set_flash('success', 'Registro eliminado correctamente.')

    return HttpResponseRedirect(reverse('carrera'))
