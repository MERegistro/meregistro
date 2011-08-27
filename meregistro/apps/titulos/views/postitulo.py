# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import Postitulo
from apps.titulos.forms import PostituloFormFilters, PostituloForm
from apps.registro.models import Anexo
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 50

def build_query(filters, page, request):
    "Construye el query de búsqueda a partir de los filtros."
    return filters.buildQuery().order_by('id').filter(anexo__ambito__path__istartswith = request.get_perfil().ambito.path)

@login_required
@credential_required('tit_postitulo_consulta')
def index(request):
    if request.method == 'GET':
        form_filter = PostituloFormFilters(request.GET)
    else:
        form_filter = PostituloFormFilters()
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
    return my_render(request, 'titulos/postitulo/index.html', {
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


@credential_required('tit_postitulo_alta')
def create(request):
    if request.method == 'POST':
        form = PostituloForm(request.POST)
        if form.is_valid():
            postitulo = form.save()
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('postituloEdit', args = [postitulo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = PostituloForm()
    form.fields["anexo"].queryset = Anexo.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    return my_render(request, 'titulos/postitulo/new.html', {
        'form': form,
        'is_new': True,
    })

@login_required
@credential_required('tit_postitulo_modificar')
def edit(request, postitulo_id):
    postitulo = Postitulo.objects.get(pk = postitulo_id)
    if request.method == 'POST':
        form = PostituloForm(request.POST, instance = postitulo)
        if form.is_valid():
            postitulo = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('postituloEdit', args = [postitulo_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = PostituloForm(instance = postitulo)

    form.fields["anexo"].queryset = Anexo.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    return my_render(request, 'titulos/postitulo/edit.html', {
        'form': form,
        'is_new': False,
    })

@credential_required('tit_postitulo_eliminar')
def delete(request, postitulo_id):
    postitulo = Postitulo.objects.get(pk=postitulo_id)
    request.set_flash('success', 'Registro eliminado correctamente.')
    postitulo.delete()
    return HttpResponseRedirect(reverse('postitulo'))
