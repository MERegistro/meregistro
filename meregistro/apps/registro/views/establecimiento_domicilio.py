# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Localidad import Localidad
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.EstablecimientoDomicilio import EstablecimientoDomicilio
from apps.registro.forms.EstablecimientoDomicilioForm import EstablecimientoDomicilioForm
from apps.registro.forms.EstablecimientoDomicilioFormFilters import EstablecimientoDomicilioFormFilters

ITEMS_PER_PAGE = 50


def __get_establecimiento_actual(request):
    """
    Trae el único establecimiento que tiene asignado, por ejemplo, un rector/director
    """
    try:
        establecimiento = Establecimiento.objects.get(ambito__path=request.get_perfil().ambito.path)
    except Establecimiento.DoesNotExist:
        raise Exception('ERROR: El usuario no tiene asignado un establecimiento.')

    return establecimiento


@login_required
@credential_required('reg_establecimiento_completar')
def index(request):

    establecimiento = __get_establecimiento_actual(request)

    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = EstablecimientoDomicilioFormFilters(request.GET, establecimiento_id=establecimiento.id)
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
    return my_render(request, 'registro/establecimiento/domicilios/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('calle', 'altura')


@login_required
@credential_required('reg_establecimiento_completar')
def create(request):
    """
    Alta de domicilio.
    """
    establecimiento = __get_establecimiento_actual(request)
    jurisdiccion = establecimiento.dependencia_funcional.jurisdiccion

    if request.method == 'POST':
        form = EstablecimientoDomicilioForm(request.POST, jurisdiccion_id=jurisdiccion.id)
        if form.is_valid():
            domicilio = form.save(commit=False)
            domicilio.establecimiento_id = establecimiento.id
            domicilio.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoDomicilioEdit', args=[domicilio.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoDomicilioForm(jurisdiccion_id=jurisdiccion.id)
    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)
    return my_render(request, 'registro/establecimiento/domicilios/new.html', {
        'form': form,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def edit(request, domicilio_id):
    """
    Edición de los datos de una domicilio.
    """
    establecimiento = __get_establecimiento_actual(request)
    domicilio = EstablecimientoDomicilio.objects.get(pk=domicilio_id, establecimiento__id=establecimiento.id)
    jurisdiccion = establecimiento.dependencia_funcional.jurisdiccion

    if request.method == 'POST':
        form = EstablecimientoDomicilioForm(request.POST, instance=domicilio, jurisdiccion_id=jurisdiccion.id)
        if form.is_valid():
            domicilio = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoDomicilioForm(instance=domicilio, jurisdiccion_id=jurisdiccion.id)

    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)
    return my_render(request, 'registro/establecimiento/domicilios/edit.html', {
        'form': form,
        'domicilio': domicilio,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def delete(request, domicilio_id):
    establecimiento = __get_establecimiento_actual(request)
    domicilio = EstablecimientoDomicilio.objects.get(pk=domicilio_id, establecimiento__id=establecimiento.id)
    domicilio.delete()
    request.set_flash('success', 'Datos del domicilio eliminados correctamente.')
    return HttpResponseRedirect(reverse('establecimientoDomiciliosIndex'))
