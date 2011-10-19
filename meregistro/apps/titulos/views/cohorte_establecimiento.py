# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import CohorteEstablecimiento, EstadoCohorteEstablecimiento, CohorteEstablecimientoSeguimiento, EstadoTituloJurisdiccional
from apps.titulos.forms import AceptarCohorteEstablecimientoFormFilters, CohorteEstablecimientoConfirmarForm, CohorteEstablecimientoSeguimientoForm
from apps.registro.models import Jurisdiccion, Establecimiento
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50

"""
Método para aplanar las listas
"""
def __flat_list(list_to_flat):
    return [i for j in list_to_flat for i in j]


def __get_establecimiento_actual(request):
    """
    Trae el único establecimiento que tiene asignado, por ejemplo, un rector/director
    """
    try:
        establecimiento = Establecimiento.objects.get(ambito__id = request.get_perfil().ambito.id)
        if not bool(establecimiento):
            raise Exception('ERROR: El usuario no tiene asignado un establecimiento.')
        else:
            return establecimiento
    except Exception:
        pass

def build_confirmar_cohortes_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    establecimiento = __get_establecimiento_actual(request)
    estado = EstadoTituloJurisdiccional.objects.get(nombre = EstadoTituloJurisdiccional.CONTROLADO)
    # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
    return filters.buildQuery().filter(establecimiento = establecimiento, cohorte__titulo_jurisdiccional__estado__nombre = estado).order_by('cohorte__titulo_jurisdiccional__titulo__nombre', '-cohorte__anio')

@login_required
@credential_required('tit_cohorte_aceptar_asignacion')
def index(request):
    """
    Index de cohorte establecimiento
    """
    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'GET':
        form_filter = AceptarCohorteEstablecimientoFormFilters(request.GET)
    else:
        form_filter = AceptarCohorteEstablecimientoFormFilters()
    q = build_confirmar_cohortes_query(form_filter, 1, request)

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
    return my_render(request, 'titulos/cohorte/cohorte_establecimiento/index.html', {
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
@credential_required('tit_cohorte_aceptar_asignacion')
def confirmar(request, cohorte_establecimiento_id):
    """
    Confirmar cohorte
    """
    cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk = cohorte_establecimiento_id)

    if request.method == 'POST':
        form = CohorteEstablecimientoConfirmarForm(request.POST, instance = cohorte_establecimiento)
        if form.is_valid():
            cohorte_establecimiento = form.save(commit = False)
            estado = EstadoCohorteEstablecimiento.objects.get(nombre = EstadoCohorteEstablecimiento.ACEPTADA)
            cohorte_establecimiento.estado = estado
            cohorte_establecimiento.save()
            cohorte_establecimiento.registrar_estado()

            request.set_flash('success', 'La cohorte fue confirmada correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('cohorteEstablecimientoIndex'))

        else:
            request.set_flash('warning', 'Ocurrió un error confirmando la cohorte.')
    else:
        form = CohorteEstablecimientoConfirmarForm(instance = cohorte_establecimiento)


    return my_render(request, 'titulos/cohorte/cohorte_establecimiento/confirmar.html', {
        'cohorte_establecimiento': cohorte_establecimiento,
        'cohorte': cohorte_establecimiento.cohorte,
        'form': form,
    })

@login_required
@credential_required('tit_cohorte_seguimiento')
def seguimiento(request, cohorte_establecimiento_id):
    """
    Seguimiento de cohorte establecimiento
    """
    establecimiento = __get_establecimiento_actual(request)
    cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk = cohorte_establecimiento_id)

    if cohorte_establecimiento.inscriptos is None: # No aceptada
        request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
        return HttpResponseRedirect(reverse('cohorteEstablecimientoIndex'))

    objects = CohorteEstablecimientoSeguimiento.objects.filter(cohorte_establecimiento = cohorte_establecimiento).order_by('anio')
    return my_render(request, 'titulos/cohorte/cohorte_establecimiento/seguimiento.html', {
        'objects': objects,
        'cohorte_establecimiento': cohorte_establecimiento,
        'page_title': 'Seguimiento de cohote',
        'actual_page': 'seguimiento',
    })

@login_required
@credential_required('tit_cohorte_seguimiento')
def create_seguimiento(request, cohorte_establecimiento_id):

    cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk = cohorte_establecimiento_id)
    if cohorte_establecimiento.inscriptos is None: # No aceptada
        request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
        return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args = [cohorte_establecimiento.id]))


    if request.method == 'POST':
        form = CohorteEstablecimientoSeguimientoForm(request.POST, inscriptos_total = cohorte_establecimiento.inscriptos, anio_cohorte = cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id = cohorte_establecimiento.id)
        if form.is_valid():
            seguimiento = form.save(commit = False)
            seguimiento.cohorte_establecimiento = cohorte_establecimiento
            seguimiento.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args = [cohorte_establecimiento.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteEstablecimientoSeguimientoForm(inscriptos_total = cohorte_establecimiento.inscriptos, anio_cohorte = cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id = cohorte_establecimiento.id)

    return my_render(request, 'titulos/cohorte/cohorte_establecimiento/new.html', {
        'form': form,
        'cohorte_establecimiento': cohorte_establecimiento,
        'form_template': 'titulos/cohorte/cohorte_establecimiento/form_seguimiento.html',
        'page_title': 'Datos de seguimiento',
        'actual_page': 'datos_seguimiento',
    })

@login_required
@credential_required('tit_cohorte_seguimiento')
def edit_seguimiento(request, seguimiento_id):
    """
    Confirmar cohorte
    """
    seguimiento = CohorteEstablecimientoSeguimiento.objects.get(pk = seguimiento_id)
    cohorte_establecimiento = seguimiento.cohorte_establecimiento

    if request.method == 'POST':
        form = CohorteEstablecimientoSeguimientoForm(request.POST, instance = seguimiento, inscriptos_total = cohorte_establecimiento.inscriptos, anio_cohorte = cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id = cohorte_establecimiento.id)
        if form.is_valid():
            seguimiento = form.save(commit = False)
            seguimiento.cohorte_establecimiento = cohorte_establecimiento
            seguimiento.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args = [cohorte_establecimiento.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteEstablecimientoSeguimientoForm(instance = seguimiento, inscriptos_total = cohorte_establecimiento.inscriptos, anio_cohorte = cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id = cohorte_establecimiento.id)

    return my_render(request, 'titulos/cohorte/cohorte_establecimiento/edit.html', {
        'form': form,
        'cohorte_establecimiento': cohorte_establecimiento,
        'form_template': 'titulos/cohorte/cohorte_establecimiento/form_seguimiento.html',
        'page_title': 'Datos de seguimiento',
        'actual_page': 'datos_seguimiento',
    })

@login_required
@credential_required('tit_cohorte_seguimiento')
def eliminar(request, seguimiento_id):
    """
    Eliminación de año de seguimiento de cohorte
    """
    seguimiento = CohorteEstablecimientoSeguimiento.objects.get(pk = seguimiento_id)

    if request.method == 'POST':
        if int(request.POST['seguimiento_id']) is not int(seguimiento.id):
            raise Exception('Error en la consulta!')

        seguimiento.delete()
        request.set_flash('success', 'El año de seguimiento fue eliminado correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args = [seguimiento.cohorte_establecimiento.id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el año de seguimiento? Esta operación no puede deshacerse.')
    return my_render(request, 'titulos/cohorte/cohorte_establecimiento/eliminar.html', {
        'seguimiento_id': seguimiento.id,
    })
