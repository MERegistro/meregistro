# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required, credential_required
from seguridad.models import Usuario, Perfil
from meregistro.registro.models.Establecimiento import Establecimiento
from meregistro.registro.models.Localidad import Localidad
from meregistro.registro.models.Estado import Estado
from meregistro.registro.models.UnidadExtension import UnidadExtension
from meregistro.registro.models.UnidadExtensionEstado import UnidadExtensionEstado
from meregistro.registro.models.UnidadExtensionDomicilio import UnidadExtensionDomicilio
from meregistro.registro.models.UnidadExtensionBaja import UnidadExtensionBaja
from meregistro.registro.forms import UnidadExtensionFormFilters, UnidadExtensionForm, UnidadExtensionDomicilioForm, UnidadExtensionBajaForm
from django.core.paginator import Paginator
from meregistro.registro.helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50

"""
La unidad de extensión pertenece al establecimiento?
"""
def __pertenece_al_establecimiento(request, unidad_extension):
    return unidad_extension.establecimiento.ambito.path == request.get_perfil().ambito.path

"""
Trae el único establecimiento que tiene asignado, por ejemplo, un rector/director
"""
def __get_establecimiento_actual(request):
    try:
        establecimiento = Establecimiento.objects.get(ambito__path = request.get_perfil().ambito.path)
        if not bool(establecimiento):
            raise Exception('ERROR: El usuario no tiene asignado un establecimiento.')
        else:
            return establecimiento
    except Exception:
        pass

@login_required
@credential_required('reg_unidad_extension_consulta')
def index(request):
    """
    Búsqueda de unidades de extensión
    """
    if request.method == 'GET':
        form_filter = UnidadExtensionFormFilters(request.GET)
    else:
        form_filter = UnidadExtensionFormFilters()
    q = build_query(form_filter, 1, request)

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id = jurisdiccion.id)
    form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
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
    return my_render(request, 'registro/unidad_extension/index.html', {
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
    return filters.buildQuery().order_by('nombre').filter(establecimiento__ambito__path__istartswith = request.get_perfil().ambito.path)


@login_required
@credential_required('reg_unidad_extension_alta')
def create(request):
    """
    Alta de unidad de extensión.
    """
    establecimiento = __get_establecimiento_actual(request)
    if request.method == 'POST':
        form = UnidadExtensionForm(request.POST)
        domicilio_form = UnidadExtensionDomicilioForm(request.POST)
        if form.is_valid() and domicilio_form.is_valid():

            unidad_extension = form.save(commit = False)
            unidad_extension.establecimiento = establecimiento
            unidad_extension.save()

            domicilio = domicilio_form.save(commit = False)
            domicilio.unidad_extension = unidad_extension
            domicilio.save()

            estado = Estado.objects.get(nombre = Estado.VIGENTE)
            unidad_extension.registrar_estado(estado)

            MailHelper.notify_by_email(MailHelper.UNIDAD_EXTENSION_CREATE, unidad_extension)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('unidadExtensionEdit', args = [unidad_extension.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = UnidadExtensionForm()
        domicilio_form = UnidadExtensionDomicilioForm()

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)

    return my_render(request, 'registro/unidad_extension/new.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'is_new': True,
    })


@login_required
@credential_required('reg_unidad_extension_modificar')
def edit(request, unidad_extension_id):
    """
    Edición de los datos de una unidad de extensión.
    """
    unidad_extension = UnidadExtension.objects.get(pk = unidad_extension_id)
    domicilio = unidad_extension.unidad_extension_domicilio.get()

    if unidad_extension.dadaDeBaja():
        raise Exception('La unidad de extensión se encuentra dada de baja.')

    if not __pertenece_al_establecimiento(request, unidad_extension):
        raise Exception('La unidad de extensión no pertenece a su establecimiento.')

    if request.method == 'POST':
        form = UnidadExtensionForm(request.POST, instance = unidad_extension)
        domicilio_form = UnidadExtensionDomicilioForm(request.POST, instance = domicilio)
        if form.is_valid() and domicilio_form.is_valid():
            unidad_extension = form.save()
            domicilio = domicilio_form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = UnidadExtensionForm(instance = unidad_extension)
        domicilio_form = UnidadExtensionDomicilioForm(instance = domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)

    return my_render(request, 'registro/unidad_extension/edit.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'domicilio': domicilio,
        'unidad_extension': unidad_extension,
    })

@login_required
@credential_required('reg_unidad_extension_baja')
def baja(request, unidad_extension_id):
    """
    Baja de un unidad de extensión
    CU 28
    """
    unidad_extension = UnidadExtension.objects.get(pk = unidad_extension_id)
    """ Pertenece al establecimiento? """
    pertenece_al_establecimiento = __pertenece_al_establecimiento(request, unidad_extension)
    if not pertenece_al_establecimiento:
        raise Exception('La unidad de extensión no pertenece al establecimiento.')
    """ La unidad de extensión ya fue dada de baja? """
    dada_de_baja = unidad_extension.dadaDeBaja()
    if dada_de_baja:
        request.set_flash('notice', 'La unidad de extensión ya se encuentra dada de baja.')
    """ Continuar """
    if request.method == 'POST':
        form = UnidadExtensionBajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit = False)
            unidad_extension.registrarBaja(baja)
            dada_de_baja = True
            request.set_flash('success', 'La unidad de extensión fue dada de baja correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('unidadExtensionBaja', args = [unidad_extension_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error dando de baja la unidad de extensión.')
    else:
        form = UnidadExtensionBajaForm()
    return my_render(request, 'registro/unidad_extension/baja.html', {
        'form': form,
        'unidad_extension': unidad_extension,
        'dada_de_baja': dada_de_baja,
    })
