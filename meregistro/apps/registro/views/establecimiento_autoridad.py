# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.EstablecimientoAutoridad import EstablecimientoAutoridad
from apps.registro.forms.EstablecimientoAutoridadForm import EstablecimientoAutoridadForm
from apps.registro.forms.EstablecimientoAutoridadFormFilters import EstablecimientoAutoridadFormFilters

ITEMS_PER_PAGE = 50


def __get_establecimiento_actual(request):
    """
    Trae el único establecimiento que tiene asignado, por ejemplo, un rector/director
    """
    establecimientos = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path)
    if len(establecimientos) == 0:
        raise Exception('ERROR: El usuario no tiene asignado un establecimiento.')
    elif len(establecimientos) == 1:
        return establecimientos[0]
    else:
        if request.session.has_key('establecimiento_seleccionado_id'):
            return Establecimiento.objects.get(pk=int(request.session['establecimiento_seleccionado_id']))
        else:
            request.set_flash('warning', 'Debe seleccionar un establecimiento.')



@login_required
#@credential_required('reg_establecimiento_ver')
def index(request):

    establecimiento = __get_establecimiento_actual(request)

    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = EstablecimientoAutoridadFormFilters(request.GET, establecimiento_id=establecimiento.id)
    else:
        form_filter = EstablecimientoFormFilters(establecimiento_id=establecimiento.id)

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
    return my_render(request, 'registro/establecimiento/autoridades/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'establecimiento': establecimiento
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery()


@login_required
@credential_required('reg_establecimiento_completar')
def create(request):
    """
    Alta de autoridad.
    """
    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'POST':
        form = EstablecimientoAutoridadForm(request.POST)
        if form.is_valid():
            autoridad = form.save(commit=False)
            autoridad.establecimiento_id = establecimiento.id
            autoridad.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoAutoridadEdit', args=[autoridad.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoAutoridadForm()
    return my_render(request, 'registro/establecimiento/autoridades/new.html', {
        'form': form,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def edit(request, autoridad_id):
    """
    Edición de los datos de una autoridad.
    """
    establecimiento = __get_establecimiento_actual(request)
    autoridad = EstablecimientoAutoridad.objects.get(pk=autoridad_id, establecimiento__id=establecimiento.id)

    if request.method == 'POST':
        form = EstablecimientoAutoridadForm(request.POST, instance=autoridad)
        if form.is_valid():
            autoridad = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoAutoridadForm(instance=autoridad)

    return my_render(request, 'registro/establecimiento/autoridades/edit.html', {
        'form': form,
        'autoridad': autoridad,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def delete(request, autoridad_id):
    establecimiento = __get_establecimiento_actual(request)
    autoridad = EstablecimientoAutoridad.objects.get(pk=autoridad_id, establecimiento__id=establecimiento.id)
    autoridad.delete()
    request.set_flash('success', 'Datos de la autoridad eliminados correctamente.')
    return HttpResponseRedirect(reverse('establecimientoAutoridadesIndex'))
