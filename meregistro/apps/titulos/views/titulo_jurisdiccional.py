# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import Titulo, TituloJurisdiccional, EstadoTituloJurisdiccional, EstadoTitulo, \
    TituloJurisdiccionalModalidadDistancia, TituloJurisdiccionalModalidadPresencial, EstadoTituloOrientacion
from apps.titulos.forms import TituloJurisdiccionalFormFilters, TituloJurisdiccionalForm, TituloJurisdiccionalDatosBasicosForm, \
    TituloJurisdiccionalOrientacionesForm, TituloJurisdiccionalModalidadPresencialForm, TituloJurisdiccionalModalidadDistanciaForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50

def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(jurisdiccion = request.get_perfil().jurisdiccion()).order_by('id')

@login_required
@credential_required('tit_titulo_jurisdiccional_consulta')
def index(request):
    """
    Búsqueda de titulos
    """
    if request.method == 'GET':
        form_filter = TituloJurisdiccionalFormFilters(request.GET)
    else:
        form_filter = TituloJurisdiccionalFormFilters()
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
    return my_render(request, 'titulos/titulo_jurisdiccional/index.html', {
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
@credential_required('tit_titulo_jurisdiccional_alta')
def create(request):
    """
    Alta de título jurisdiccional.
    """
    if request.method == 'POST':
        form = TituloJurisdiccionalDatosBasicosForm(request.POST)
        if form.is_valid():
            titulo_jurisdiccional = form.save(commit = False)
            titulo_jurisdiccional.estado = EstadoTituloJurisdiccional.objects.get(nombre = EstadoTituloJurisdiccional.CONTROLADO)
            titulo_jurisdiccional.jurisdiccion = request.get_perfil().jurisdiccion()
            titulo_jurisdiccional.save()
            #form.save_m2m() # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
            titulo_jurisdiccional.registrar_estado()

            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalEdit', args = [titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloJurisdiccionalDatosBasicosForm()
    # Agrego el filtro por jurisdicción
    form.fields['titulo'].queryset = form.fields['titulo'].queryset.filter(jurisdicciones__id = request.get_perfil().jurisdiccion().id)
    return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'form': form,
        'form_template': 'titulos/titulo_jurisdiccional/form_datos_basicos.html',
        'is_new': True,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })

@login_required
@credential_required('tit_titulo_jurisdiccional_modificar')
# Editar datos básicos
def edit(request, titulo_jurisdiccional_id):
    """
    Edición de los datos de un título jurisdiccional.
    """
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
    titulo_anterior_id = int(titulo_jurisdiccional.titulo_id)

    if request.method == 'POST':
        form = TituloJurisdiccionalDatosBasicosForm(request.POST, instance = titulo_jurisdiccional)
        if form.is_valid():

            # Cambió el título? Borrar las orientaciones
            cambio_titulo = titulo_anterior_id is not int(request.POST['titulo'])
            if cambio_titulo:
                titulo_jurisdiccional.eliminar_orientaciones()

            titulo_jurisdiccional = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = TituloJurisdiccionalDatosBasicosForm(instance = titulo_jurisdiccional)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_datos_basicos.html',
        'is_new': False,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })

@login_required
@credential_required('tit_titulo_jurisdiccional_alta')
@credential_required('tit_titulo_jurisdiccional_modificar')
def editar_orientaciones(request, titulo_jurisdiccional_id):
    """
    Edición de orientaciones del título jurisdiccional.
    """
    try:
        titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'titulo_jurisdiccional': None,
        'form_template': 'titulos/titulo_jurisdiccional/form_orientaciones.html',
        'page_title': 'Orientaciones',
        'actual_page': 'orientaciones',
    })

    if request.method == 'POST':
        form = TituloJurisdiccionalOrientacionesForm(request.POST, instance = titulo_jurisdiccional)
        if form.is_valid():
            orientaciones = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalOrientacionesEdit', args = [titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloJurisdiccionalOrientacionesForm(instance = titulo_jurisdiccional)

    form.fields['orientaciones'].queryset = form.fields['orientaciones'].queryset.filter(titulo = titulo_jurisdiccional.titulo, estado__nombre = EstadoTituloOrientacion.VIGENTE)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_orientaciones.html',
        'is_new': False,
        'page_title': 'Orientaciones',
        'actual_page': 'orientaciones',
    })

@login_required
@credential_required('tit_titulo_jurisdiccional_alta')
@credential_required('tit_titulo_jurisdiccional_modificar')
def editar_modalidades(request, titulo_jurisdiccional_id):
    """
    Edición de modalidades del título jurisdiccional.
    """
    try:
        titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'titulo_jurisdiccional': None,
        'form_template': 'titulos/titulo_jurisdiccional/form_modalidades.html',
        'page_title': 'Modalidades',
        'actual_page': 'modalidades',
    })

    # Ya existen los objectos relacionados?
    try:
        modalidad_presencial = titulo_jurisdiccional.modalidad_presencial.get()
    except:
        modalidad_presencial = TituloJurisdiccionalModalidadPresencial(titulo = titulo_jurisdiccional)

    try:
        modalidad_distancia = titulo_jurisdiccional.modalidad_distancia.get()
    except:
        modalidad_distancia = TituloJurisdiccionalModalidadDistancia(titulo = titulo_jurisdiccional)

    # Prefixes de los inputs para no confundir los formularios
    prefix_mod_presencial = 'mod_presencial'
    prefix_mod_distancia = 'mod_distancia'

    if request.method == 'POST':
        form_modalidad_presencial = TituloJurisdiccionalModalidadPresencialForm(request.POST, instance = modalidad_presencial, prefix = prefix_mod_presencial)
        form_modalidad_distancia = TituloJurisdiccionalModalidadDistanciaForm(request.POST, instance = modalidad_distancia, prefix = prefix_mod_distancia)

        if form_modalidad_presencial.is_valid() and form_modalidad_distancia.is_valid():
            # Eliminarlo si se des-checkeó el checkbox y ya existe el objecto
            try:
                if request.POST['mod_presencial-posee_mod_presencial'] == 'on':
                    modalidad_presencial = form_modalidad_presencial.save()
            except KeyError: # No se activó el checkbox
                if modalidad_presencial.id:
                    modalidad_presencial.delete()

            try:
                if request.POST['mod_distancia-posee_mod_distancia'] != 'on' and modalidad_distancia.id:
                    #raise Exception('a')
                    modalidad_distancia.delete()
                else:
                    #raise Exception('b')
                    modalidad_distancia = form_modalidad_distancia.save()
            except KeyError: # No se activó el checkbox
                #raise Exception('c')
                if modalidad_distancia.id:
                    modalidad_distancia.delete()

            #if request.POST['mod_distancia-posee_mod_distancia'] != 'on' and modalidad_distancia.id:
            #    modalidad_distancia.delete()
            #else:
            #    modalidad_distancia = form_modalidad_distancia.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalModalidadesEdit', args = [titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form_modalidad_presencial = TituloJurisdiccionalModalidadPresencialForm(instance = modalidad_presencial, prefix = prefix_mod_presencial)
        form_modalidad_distancia = TituloJurisdiccionalModalidadDistanciaForm(instance = modalidad_distancia, prefix = prefix_mod_distancia)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'modalidad_presencial': modalidad_presencial,
        'modalidad_distancia': modalidad_distancia,
        'form_modalidad_presencial': form_modalidad_presencial,
        'form_modalidad_distancia': form_modalidad_distancia,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_modalidades.html',
        'is_new': False,
        'page_title': 'Modalidades',
        'actual_page': 'modalidades',
    })

@login_required
@credential_required('tit_titulo_jurisdiccional_eliminar')
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
