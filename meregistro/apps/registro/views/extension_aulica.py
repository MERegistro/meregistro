# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Localidad import Localidad
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.ExtensionAulicaEstado import ExtensionAulicaEstado
from apps.registro.models.ExtensionAulicaDomicilio import ExtensionAulicaDomicilio
from apps.registro.models.ExtensionAulicaBaja import ExtensionAulicaBaja
from apps.registro.forms import ExtensionAulicaFormFilters, ExtensionAulicaForm, ExtensionAulicaDomicilioForm, ExtensionAulicaBajaForm
from helpers.MailHelper import MailHelper
from django.core.paginator import Paginator
import datetime

ITEMS_PER_PAGE = 50

"""
La extensión áulica pertenece al establecimiento?
"""
def __pertenece_al_establecimiento(request, extension_aulica):
    return extension_aulica.establecimiento.ambito.path == request.get_perfil().ambito.path

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
@credential_required('reg_extension_aulica_consulta')
def index(request):
    """
    Búsqueda de extensiones áulicas
    """
    if request.method == 'GET':
        form_filter = ExtensionAulicaFormFilters(request.GET)
    else:
        form_filter = ExtensionAulicaFormFilters()
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
    return my_render(request, 'registro/extension_aulica/index.html', {
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
@credential_required('reg_extension_aulica_alta')
def create(request):
    """
    Alta de extensión áulica.
    """
    establecimiento = __get_establecimiento_actual(request)
    if request.method == 'POST':
        form = ExtensionAulicaForm(request.POST)
        domicilio_form = ExtensionAulicaDomicilioForm(request.POST)
        if form.is_valid() and domicilio_form.is_valid():

            extension_aulica = form.save(commit = False)
            estado = EstadoExtensionAulica.objects.get(nombre = EstadoExtensionAulica.VIGENTE)
            extension_aulica.estado = estado
            extension_aulica.establecimiento = establecimiento
            extension_aulica.save()
            extension_aulica.registrar_estado()

            form.save_m2m() # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
            
            domicilio = domicilio_form.save(commit = False)
            domicilio.extension_aulica = extension_aulica
            domicilio.save()

            MailHelper.notify_by_email(MailHelper.EXTENSION_AULICA_CREATE, extension_aulica)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('extensionAulicaEdit', args = [extension_aulica.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = ExtensionAulicaForm()
        domicilio_form = ExtensionAulicaDomicilioForm()

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)

    return my_render(request, 'registro/extension_aulica/new.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'is_new': True,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def edit(request, extension_aulica_id):
    """
    Edición de los datos de una extensión áulica.
    """
    extension_aulica = ExtensionAulica.objects.get(pk = extension_aulica_id)
    domicilio = extension_aulica.domicilio.get()

    if extension_aulica.dadaDeBaja():
        raise Exception('La extensión áulica se encuentra dada de baja.')

    if not __pertenece_al_establecimiento(request, extension_aulica):
        raise Exception('La extensión áulica no pertenece a su establecimiento.')

    if request.method == 'POST':
        form = ExtensionAulicaForm(request.POST, instance = extension_aulica)
        domicilio_form = ExtensionAulicaDomicilioForm(request.POST, instance = domicilio)
        if form.is_valid() and domicilio_form.is_valid():
            extension_aulica = form.save()
            domicilio = domicilio_form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaForm(instance = extension_aulica)
        domicilio_form = ExtensionAulicaDomicilioForm(instance = domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)

    return my_render(request, 'registro/extension_aulica/edit.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'domicilio': domicilio,
        'extension_aulica': extension_aulica,
    })

@login_required
@credential_required('reg_extension_aulica_baja')
def baja(request, extension_aulica_id):
    """
    Baja de un extensión áulica
    CU 28
    """
    extension_aulica = ExtensionAulica.objects.get(pk = extension_aulica_id)
    """ Pertenece al establecimiento? """
    pertenece_al_establecimiento = __pertenece_al_establecimiento(request, extension_aulica)
    if not pertenece_al_establecimiento:
        raise Exception('La extensión áulica no pertenece al establecimiento.')
    """ La extensión áulica ya fue dada de baja? """
    dada_de_baja = extension_aulica.dadaDeBaja()
    if dada_de_baja:
        request.set_flash('notice', 'La extensión áulica ya se encuentra dada de baja.')
    """ Continuar """
    if request.method == 'POST':
        form = ExtensionAulicaBajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit = False)
            baja.extension_aulica = extension_aulica
            baja.save()
            estado = EstadoExtensionAulica.objects.get(nombre = EstadoExtensionAulica.BAJA)
            extension_aulica.estado = estado
            extension_aulica.save()
            extension_aulica.registrar_estado()

            dado_de_baja = True

            request.set_flash('success', 'La extensión áulica fue dada de baja correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('extension_aulica'))
        else:
            request.set_flash('warning', 'Ocurrió un error dando de baja la extensión áulica.')
    else:
        form = ExtensionAulicaBajaForm()
    return my_render(request, 'registro/extension_aulica/baja.html', {
        'form': form,
        'extension_aulica': extension_aulica,
        'dada_de_baja': dada_de_baja,
    })
