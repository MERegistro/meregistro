# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import Titulo, TituloJurisdiccional, EstadoTituloJurisdiccional, EstadoTitulo, TituloOrientacion, \
    EstadoTituloOrientacion, EstadoNormativaJurisdiccional, \
    TituloJurisdiccionalCohorte
from apps.titulos.forms import TituloJurisdiccionalFormFilters, TituloJurisdiccionalForm, TituloJurisdiccionalDatosBasicosForm, \
    TituloJurisdiccionalOrientacionesForm, \
    TituloJurisdiccionalDuracionForm, TituloJurisdiccionalNormativasForm, TituloJurisdiccionalCohorteForm
from apps.registro.models import Jurisdiccion
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper

ITEMS_PER_PAGE = 50


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(jurisdiccion=request.get_perfil().jurisdiccion()).order_by('id')


@login_required
#@credential_required('tit_titulo_jurisdiccional_consulta')
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
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


@login_required
@credential_required('tit_carrera_jurisdiccional_alta')
def create(request):
    """
    Alta de título jurisdiccional.
    """
    if request.method == 'POST':
        form = TituloJurisdiccionalDatosBasicosForm(request.POST, jurisdiccion_id=request.get_perfil().jurisdiccion().id)
        if form.is_valid():
            titulo_jurisdiccional = form.save(commit=False)
            titulo_jurisdiccional.estado = EstadoTituloJurisdiccional.objects.get(nombre=EstadoTituloJurisdiccional.REGISTRADO)
            titulo_jurisdiccional.jurisdiccion = request.get_perfil().jurisdiccion()
            titulo_jurisdiccional.save()
            #form.save_m2m() # Guardo las relaciones - https://docs.djangoproject.com/en/1.2/topics/forms/modelforms/#the-save-method
            titulo_jurisdiccional.registrar_estado()

            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalEdit', args=[titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloJurisdiccionalDatosBasicosForm(jurisdiccion_id=request.get_perfil().jurisdiccion().id)
    # Agrego el filtro por jurisdicción
    return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'form': form,
        'form_template': 'titulos/titulo_jurisdiccional/form_datos_basicos.html',
        'is_new': True,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })


@login_required
#@credential_required('tit_titulo_jurisdiccional_modificar')
# Editar datos básicos
def edit(request, titulo_jurisdiccional_id):
    """
    Edición de los datos de un título jurisdiccional.
    """
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)
    titulo_anterior_id = int(titulo_jurisdiccional.carrera_id)

    if request.method == 'POST':
        form = TituloJurisdiccionalDatosBasicosForm(request.POST, instance=titulo_jurisdiccional, jurisdiccion_id=request.get_perfil().jurisdiccion().id)
        if form.is_valid():

            # Cambió el título? Borrar las orientaciones
            cambio_titulo = titulo_anterior_id is not int(request.POST['carrera'])
            if cambio_titulo:
                titulo_jurisdiccional.eliminar_orientaciones()

            titulo_jurisdiccional = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = TituloJurisdiccionalDatosBasicosForm(instance=titulo_jurisdiccional, jurisdiccion_id=request.get_perfil().jurisdiccion().id)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_datos_basicos.html',
        'is_new': False,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })


@login_required
#@credential_required('tit_titulo_jurisdiccional_alta')
#@credential_required('tit_titulo_jurisdiccional_modificar')
def editar_orientaciones(request, titulo_jurisdiccional_id):
    """
    Edición de orientaciones del título jurisdiccional.
    """
    try:
        titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'titulo_jurisdiccional': None,
        'form_template': 'titulos/titulo_jurisdiccional/form_orientaciones.html',
        'page_title': 'Orientaciones',
        'actual_page': 'orientaciones',
    })

    if request.method == 'POST':
        form = TituloJurisdiccionalOrientacionesForm(request.POST, instance=titulo_jurisdiccional)
        if form.is_valid():
            orientaciones = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalOrientacionesEdit', args=[titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloJurisdiccionalOrientacionesForm(instance=titulo_jurisdiccional)

    form.fields['orientaciones'].queryset = form.fields['orientaciones'].queryset.filter(titulo=titulo_jurisdiccional.titulo, estado__nombre=EstadoTituloOrientacion.VIGENTE)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_orientaciones.html',
        'is_new': False,
        'page_title': 'Orientaciones',
        'actual_page': 'orientaciones',
    })


@login_required
#@credential_required('tit_titulo_jurisdiccional_alta')
#@credential_required('tit_titulo_jurisdiccional_modificar')
def editar_normativas(request, titulo_jurisdiccional_id):
    """
    Edición de normativas del título jurisdiccional.
    """
    try:
        titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'titulo_jurisdiccional': None,
        'form_template': 'titulos/titulo_jurisdiccional/form_normativas.html',
        'page_title': 'Normativas',
        'actual_page': 'normativas',
    })

    if request.method == 'POST':
        form = TituloJurisdiccionalNormativasForm(request.POST, instance=titulo_jurisdiccional)
        if form.is_valid():
            normativas = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalNormativasEdit', args=[titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloJurisdiccionalNormativasForm(instance=titulo_jurisdiccional)

    form.fields['normativas'].queryset = form.fields['normativas'].queryset.filter(jurisdiccion=request.get_perfil().jurisdiccion, estado__nombre=EstadoNormativaJurisdiccional.VIGENTE)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_normativas.html',
        'is_new': False,
        'page_title': 'Normativas',
        'actual_page': 'normativas',
    })


@login_required
#@credential_required('tit_titulo_jurisdiccional_alta')
#@credential_required('tit_titulo_jurisdiccional_modificar')
def editar_cohortes(request, titulo_jurisdiccional_id):
    """
    Edición de datos de cohortes del título jurisdiccional.
    """
    try:
        titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'titulos/titulo_jurisdiccional/new.html', {
        'titulo_jurisdiccional': None,
        'form_template': 'titulos/titulo_jurisdiccional/form_cohortes.html',
        'page_title': 'Datos de cohortes',
        'actual_page': 'cohortes',
    })

    try:
        cohorte = TituloJurisdiccionalCohorte.objects.get(titulo_jurisdiccional=titulo_jurisdiccional)
    except:
        cohorte = TituloJurisdiccionalCohorte(titulo_jurisdiccional=titulo_jurisdiccional)

    if request.method == 'POST':
        form = TituloJurisdiccionalCohorteForm(request.POST, instance=cohorte)
        if form.is_valid():
            cohorte = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('tituloJurisdiccionalCohortesEdit', args=[titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = TituloJurisdiccionalCohorteForm(instance=cohorte)

    return my_render(request, 'titulos/titulo_jurisdiccional/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'form_template': 'titulos/titulo_jurisdiccional/form_cohortes.html',
        'is_new': False,
        'page_title': 'Datos de cohortes',
        'actual_page': 'cohortes',
    })


@login_required
#@credential_required('tit_titulo_jurisdiccional_consulta')
def orientaciones_por_titulo(request, titulo_jurisdiccional_id):
    "Búsqueda de orientaciones por título jurisdiccional"
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)
    q = TituloOrientacion.objects.filter(titulo__id=titulo_jurisdiccional.titulo_id)
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
    return my_render(request, 'titulos/titulo_jurisdiccional/orientaciones_por_titulo.html', {
        #'form_filters': form_filter,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


@login_required
#@credential_required('tit_titulo_jurisdiccional_eliminar')
def eliminar(request, titulo_id):
    """
    Baja de un título
    --- mientras no sea referido por un título jurisdiccional ---
    """
    titulo = Titulo.objects.get(pk=titulo_id)
    request.set_flash('warning', 'Está seguro de eliminar el título? Esta operación no puede deshacerse.')
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


@login_required
#@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, oid):
    o = TituloJurisdiccional.objects.get(pk=oid)
    o.revisado_jurisdiccion = True
    o.estado = EstadoTituloJurisdiccional.objects.get(nombre=EstadoTituloJurisdiccional.CONTROLADO)
    o.registrar_estado()
    request.set_flash('success', 'Registro revisado.')
    return HttpResponseRedirect(reverse('tituloJurisdiccional'))
