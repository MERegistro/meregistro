# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required, credential_required
from seguridad.models import Usuario, Perfil
from meregistro.registro.models.Establecimiento import Establecimiento
from meregistro.apps.titulos.forms import TituloFormFilters, TituloForm
from django.core.paginator import Paginator
from meregistro.registro.helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50

"""
El anexo pertenece al establecimiento?
"""
def __pertenece_al_establecimiento(request, anexo):
    return anexo.establecimiento.ambito.path == request.get_perfil().ambito.path

@login_required
#@credential_required('reg_anexo_consulta')
def index(request):
    """
    Búsqueda de titulos
    """
    if request.method == 'GET':
        form_filter = TituloFormFilters(request.GET)
    else:
        form_filter = AnexoFormFilters()
    q = build_query(form_filter, 1, request)

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        form_filter.fields["jurisdiccion"].queryset = Titulo.objects.filter(jurisdiccion__id = jurisdiccion.id)
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
    return my_render(request, 'registro/titulos/index.html', {
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
@credential_required('reg_anexo_alta')
def create(request):
    """
    Alta de anexo.
    """
    if request.method == 'POST':
        form = AnexoForm(request.POST)
        domicilio_form = AnexoDomicilioForm(request.POST)
        if form.is_valid() and domicilio_form.is_valid():
            anexo = form.save()
            domicilio = domicilio_form.save(commit = False)
            domicilio.anexo = anexo
            domicilio.save()

            estado = Estado.objects.get(nombre = Estado.VIGENTE)
            anexo.registrar_estado(estado)

            MailHelper.notify_by_email(MailHelper.ANEXO_CREATE, anexo)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('anexoEdit', args=[anexo.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = AnexoForm()
        domicilio_form = AnexoDomicilioForm()

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)

    return my_render(request, 'registro/anexo/new.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'is_new': True,
    })


@login_required
@credential_required('reg_anexo_modificar')
def edit(request, anexo_id):
    """
    Edición de los datos de un anexo.
    """
    anexo = Anexo.objects.get(pk = anexo_id)
    if anexo.dadoDeBaja():
        raise Exception('El anexo se encuentra dado de baja.')
    if not __pertenece_al_establecimiento(request, anexo):
        raise Exception('El anexo no pertenece a su establecimiento.')
    try:
        domicilio = AnexoDomicilio.objects.get(anexo = anexo)
    except:
        domicilio = AnexoDomicilio()
        domicilio.anexo = anexo
    if request.method == 'POST':
        form = AnexoForm(request.POST, instance = anexo)
        domicilio_form = AnexoDomicilioForm(request.POST, instance = domicilio)
        if form.is_valid() and domicilio_form.is_valid():
            anexo = form.save()
            domicilio = domicilio_form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoForm(instance = anexo)
        domicilio_form = AnexoDomicilioForm(instance = domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith = request.get_perfil().ambito.path)
    if jurisdiccion is not None:
        domicilio_form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id = jurisdiccion.id)
    return my_render(request, 'registro/anexo/edit.html', {
        'form': form,
        'domicilio_form': domicilio_form,
        'domicilio': domicilio,
        'anexo': anexo,
    })

@login_required
@credential_required('reg_anexo_baja')
def baja(request, anexo_id):
    """
    Baja de un anexo
    CU 28
    """
    anexo = Anexo.objects.get(pk = anexo_id)
    """ Pertenece al establecimiento? """
    pertenece_al_establecimiento = __pertenece_al_establecimiento(request, anexo)
    if not pertenece_al_establecimiento:
        raise Exception('El anexo no pertenece a su establecimiento.')
    """ El anexo ya fue dado de baja? """
    dado_de_baja = anexo.dadoDeBaja()
    if dado_de_baja:
        request.set_flash('notice', 'El anexo ya se encuentra dado de baja.')
    """ Continuar """
    if request.method == 'POST':
        form = AnexoBajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit = False)
            anexo.registrarBaja(baja)
            dado_de_baja = True
            request.set_flash('success', 'El anexo fue dado de baja correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('anexoBaja', args = [anexo_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error dando de baja el anexo.')
    else:
        form = AnexoBajaForm()
    return my_render(request, 'registro/anexo/baja.html', {
        'form': form,
        'anexo': anexo,
        'dado_de_baja': dado_de_baja,
    })
