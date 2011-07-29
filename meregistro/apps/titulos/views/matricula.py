# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import Matricula
from apps.titulos.forms import MatriculaFormFilters, MatriculaForm
from apps.registro.models import Establecimiento
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 50

def build_query(filters, page, request):
    "Construye el query de búsqueda a partir de los filtros."
    return filters.buildQuery().order_by('id').filter(establecimiento__ambito__path__istartswith = request.get_perfil().ambito.path)

@login_required
@credential_required('tit_matricula_consulta')
def index(request):
    if request.method == 'GET':
        form_filter = MatriculaFormFilters(request.GET)
    else:
        form_filter = MatriculaFormFilters()
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
    return my_render(request, 'titulos/matricula/index.html', {
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


@credential_required('tit_matricula_alta')
def create(request):
    if request.method == 'POST':
        form = MatriculaForm(request.POST)
        if form.is_valid():
            matricula = form.save()
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('matriculaEdit', args = [matricula.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = MatriculaForm()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    return my_render(request, 'titulos/matricula/new.html', {
        'form': form,
        'is_new': True,
    })

@login_required
@credential_required('tit_matricula_modificar')
def edit(request, matricula_id):
    matricula = Matricula.objects.get(pk = matricula_id)
    if request.method == 'POST':
        form = MatriculaForm(request.POST, instance = matricula)
        if form.is_valid():
            matricula = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('matriculaEdit', args = [matricula_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = MatriculaForm(instance = matricula)

    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    return my_render(request, 'titulos/matricula/edit.html', {
        'form': form,
        'is_new': False,
    })

@credential_required('tit_matricula_eliminar')
def delete(request, matricula_id):
    matricula = Matricula.objects.get(pk=matricula_id)
    if matricula.isDeletable():
        request.set_flash('success', 'Registro eliminado correctamente.')
        matricula.delete()
    else:
        request.set_flash('warning', 'No se puede eliminar la matricula.')
    return HttpResponseRedirect(reverse('matricula'))