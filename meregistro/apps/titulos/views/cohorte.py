# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import TituloJurisdiccional, Cohorte, CohorteEstablecimiento, EstadoTituloJurisdiccional, EstadoCohorteEstablecimiento
from apps.titulos.forms import TituloJurisdiccionalCohorteFormFilters, CohorteForm, CohorteAsignarEstablecimientosFormFilters,\
    AceptarCohorteFormFilters, CohorteConfirmarForm, CohorteSeguimientoForm
from apps.registro.models import Jurisdiccion, Establecimiento
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50

def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(jurisdiccion = request.get_perfil().jurisdiccion()).order_by('id')

@login_required
@credential_required('tit_cohorte_consulta')
def index(request):
    """
    Búsqueda de titulos
    """
    if request.method == 'GET':
        form_filter = TituloJurisdiccionalCohorteFormFilters(request.GET)
    else:
        form_filter = TituloJurisdiccionalCohorteFormFilters()
    q = build_query(form_filter, 1, request).filter(jurisdiccion = request.get_perfil().jurisdiccion()).order_by('id')

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
    return my_render(request, 'titulos/cohorte/index.html', {
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
@credential_required('tit_cohorte_alta')
def create(request, titulo_jurisdiccional_id = None):
    """
    Alta de cohorte
    """
    "Agregar cohorte al título actual o crearla eligiendo el mismo"
    if titulo_jurisdiccional_id is not None:
        titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
        choices = CohorteForm.ANIOS_COHORTE_CHOICES
        choices = [('', '-------')] + [(i, i) for i in range(titulo_jurisdiccional.datos_cohorte.get().anio_primera_cohorte, titulo_jurisdiccional.datos_cohorte.get().anio_ultima_cohorte + 1)]
    else:
        titulo_jurisdiccional = None
        choices = CohorteForm.ANIOS_COHORTE_CHOICES

    if request.method == 'POST':
        form = CohorteForm(request.POST)
        if form.is_valid():
            cohorte = form.save()

            # redirigir a edit
            return HttpResponseRedirect(reverse('cohortesPorTitulo', args = [cohorte.titulo_jurisdiccional.id]))
            request.set_flash('success', 'Datos guardados correctamente.')

        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteForm()

    if titulo_jurisdiccional:
        q = TituloJurisdiccional.objects.filter(id = titulo_jurisdiccional.id)
        form.fields["titulo_jurisdiccional"].empty_label = None
    else:
        # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
        q = TituloJurisdiccional.objects.filter(estado__nombre = EstadoTituloJurisdiccional.CONTROLADO, datos_cohorte__anio_ultima_cohorte__gte = datetime.date.today().year)
        form.fields["titulo_jurisdiccional"].queryset = q.filter(jurisdiccion = request.get_perfil().jurisdiccion())

    form.fields["titulo_jurisdiccional"].queryset = q
    form.fields["anio"].choices = choices

    return my_render(request, 'titulos/cohorte/new.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': True,
    })

@login_required
@credential_required('tit_cohorte_modificar')
# Editar datos básicos
def edit(request, cohorte_id):
    """
    Edición de los datos de una cohorte.
    """
    cohorte = Cohorte.objects.get(pk = cohorte_id)

    if request.method == 'POST':
        form = CohorteForm(request.POST, instance = cohorte)
        if form.is_valid():

            cohorte = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = CohorteForm(instance = cohorte)

    asignada_establecimiento = cohorte.asignada_establecimiento()
    if(asignada_establecimiento):
        # No se puede modificar el título ni el año
        form.fields["titulo_jurisdiccional"].queryset = TituloJurisdiccional.objects.filter(id = cohorte.titulo_jurisdiccional_id)
        form.fields["anio"].choices = [(cohorte.anio, cohorte.anio)]
        form.fields["titulo_jurisdiccional"].empty_label = None
    return my_render(request, 'titulos/cohorte/edit.html', {
        'form': form,
        'cohorte': cohorte,
        'titulo_jurisdiccional': cohorte.titulo_jurisdiccional,
        'asignada_establecimiento': asignada_establecimiento,
        'is_new': False,
    })


@login_required
@credential_required('tit_cohorte_consulta')
def cohortes_por_titulo(request, titulo_jurisdiccional_id):
    "Cohortes por título"
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
    q = Cohorte.objects.filter(titulo_jurisdiccional__id = titulo_jurisdiccional.id)
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
    return my_render(request, 'titulos/cohorte/cohortes_por_titulo.html', {
        'titulo_jurisdiccional': titulo_jurisdiccional,
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
@credential_required('tit_cohorte_asignar')
def asignar_establecimientos(request, cohorte_id):

    """
    Asignar cohorte a establecimientos
    """

    cohorte = Cohorte.objects.get(pk = cohorte_id)
    "Traigo los ids de los establecimientos actualmente asignados a la cohorte"
    current_establecimientos_ids = __flatten_list(CohorteEstablecimiento.objects.filter(cohorte = cohorte).values_list("establecimiento_id"))

    "Búsqueda de establecimientos"
    if request.method == 'GET':
        form_filters = CohorteAsignarEstablecimientosFormFilters(request.GET)
    else:
        form_filters = CohorteAsignarEstablecimientosFormFilters()

        # POST, guardo los datos
        post_ids = request.POST.getlist("establecimientos")
        estado = EstadoCohorteEstablecimiento.objects.get(nombre = EstadoCohorteEstablecimiento.ASIGNADA)
        cohorte.save_establecimientos(current_establecimientos_ids, post_ids, estado)

        request.set_flash('success', 'Datos actualizados correctamente.')
        # redirigir a edit
        return HttpResponseRedirect(reverse('cohorteAsignarEstablecimientos', args = [cohorte.id]))

    jurisdiccion = request.get_perfil().jurisdiccion()

    form_filters.fields["dependencia_funcional"].queryset = form_filters.fields["dependencia_funcional"].queryset.filter(jurisdiccion = jurisdiccion)
    form_filters.fields["localidad"].queryset = form_filters.fields["localidad"].queryset.filter(departamento__jurisdiccion = jurisdiccion)

    q = build_asignar_establecimientos_query(form_filters, request)

    return my_render(request, 'titulos/cohorte/asignar_establecimientos.html', {
        'cohorte': cohorte,
        'current_establecimientos_ids': current_establecimientos_ids,
        'form_filters': form_filters,
        'objects': q,
    })


def build_asignar_establecimientos_query(filters, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(ambito__path__istartswith = request.get_perfil().ambito.path)


@login_required
@credential_required('tit_cohorte_eliminar')
def eliminar(request, cohorte_id):
    """
    Baja de una cohorte
    --- mientras no estén asignadas a un establecimiento ---
    """
    cohorte = Cohorte.objects.get(pk = cohorte_id)
    asignada_establecimiento = cohorte.asignada_establecimiento()

    if asignada_establecimiento:
        request.set_flash('warning', 'La cohorte no puede darse de baja porque tiene establecimientos asignados.')
    else:
        request.set_flash('warning', 'Está seguro de eliminar la cohorte? Esta operación no puede deshacerse.')

    if request.method == 'POST':
        if int(request.POST['cohorte_id']) is not int(cohorte.id):
            raise Exception('Error en la consulta!')

        cohorte.delete()
        request.set_flash('success', 'La cohorte fue eliminada correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('cohorte'))

    return my_render(request, 'titulos/cohorte/eliminar.html', {
        'cohorte': cohorte,
        'cohorte_id': cohorte.id,
        'asignada_establecimiento': asignada_establecimiento,
    })

"""
Método para aplanar las listas
"""
def __flatten_list(list_to_flatten):
    return [i for j in list_to_flatten for i in j]


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
    return filters.buildQuery().filter(establecimiento = __get_establecimiento_actual(request))

@login_required
@credential_required('tit_cohorte_aceptar_asignacion')
def listado_para_confirmar(request):
    """
    Búsqueda de titulos para confirmar cohortes
    """

    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'GET':
        form_filter = AceptarCohorteFormFilters(request.GET)
    else:
        form_filter = AceptarCohorteFormFilters()
    q = build_confirmar_cohortes_query(form_filter, 1, request).order_by('id')

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
    return my_render(request, 'titulos/cohorte/listado_para_confirmar.html', {
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
def confirmar_cohorte(request, cohorte_establecimiento_id):
    """
    Confirmar cohorte
    """
    cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk = cohorte_establecimiento_id)

    if request.method == 'POST':
        form = CohorteConfirmarForm(request.POST, instance = cohorte_establecimiento)
        if form.is_valid():
            cohorte_establecimiento = form.save(commit = False)
            estado = EstadoCohorteEstablecimiento.objects.get(nombre = EstadoCohorteEstablecimiento.ACEPTADA)
            cohorte_establecimiento.estado = estado
            cohorte_establecimiento.save()
            cohorte_establecimiento.registrar_estado()

            request.set_flash('success', 'La cohorte fue confirmada correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('cohorteListadoParaConfirmar'))

        else:
            request.set_flash('warning', 'Ocurrió un error confirmando la cohorte.')
    else:
        form = CohorteConfirmarForm(instance = cohorte_establecimiento)


    return my_render(request, 'titulos/cohorte/confirmar.html', {
        'cohorte_establecimiento': cohorte_establecimiento,
        'form': form,
    })

@login_required
@credential_required('tit_cohorte_seguimiento')
def seguimiento_cohorte(request, cohorte_establecimiento_id):
    """
    Confirmar cohorte
    """
    cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk = cohorte_establecimiento_id)

    if request.method == 'POST':
        form = CohorteSeguimientoForm(request.POST, instance = cohorte_establecimiento)
        if form.is_valid():
            cohorte_seguimiento = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('cohorteSeguimientoHome', args = [cohorte_establecimiento.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteSeguimientoForm(instance = cohorte_establecimiento)

    return my_render(request, 'titulos/cohorte/seguimiento/index.html', {
        'form': form,
        'cohorte_establecimiento': cohorte_establecimiento,
        'form_template': 'titulos/cohorte/seguimiento/form_datos_basicos.html',
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })
