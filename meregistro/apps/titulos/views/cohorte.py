# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import TituloJurisdiccional, Cohorte, CohorteEstablecimiento, EstadoTituloJurisdiccional, EstadoCohorteEstablecimiento, \
    CohorteAnexo, EstadoCohorteAnexo, CohorteUnidadExtension, EstadoCohorteUnidadExtension
from apps.titulos.forms import TituloJurisdiccionalCohorteFormFilters, CohorteForm, CohorteAsignarEstablecimientosFormFilters, \
    CohorteAsignarAnexosFormFilters, CohorteAsignarUnidadesExtensionFormFilters
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
        choices = [('', '-------')] + [(i, i) for i in range(titulo_jurisdiccional.datos_cohorte.get().anio_primera_cohorte, titulo_jurisdiccional.datos_cohorte.get().anio_ultima_cohorte + 1)]
    else:
        titulo_jurisdiccional = None
        choices = [('', '---Seleccione un título---')]

    if request.method == 'POST':
        form = CohorteForm(request.POST)
        if form.is_valid():
            cohorte = form.save()

            # redirigir a edit
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('cohortesPorTitulo', args = [cohorte.titulo_jurisdiccional.id]))

        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = CohorteForm()

    if titulo_jurisdiccional:
        q = TituloJurisdiccional.objects.filter(id = titulo_jurisdiccional.id)
        form.fields["titulo_jurisdiccional"].empty_label = None
    else:
        # Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
        #q = TituloJurisdiccional.objects.filter(estado__nombre = EstadoTituloJurisdiccional.CONTROLADO, datos_cohorte__anio_ultima_cohorte__lte = datetime.date.today().year)
        q = TituloJurisdiccional.objects.filter(estado__nombre = EstadoTituloJurisdiccional.CONTROLADO)
        form.fields["titulo_jurisdiccional"].queryset = q.filter(jurisdiccion = request.get_perfil().jurisdiccion()).order_by('titulo__nombre')

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

    titulo_jurisdiccional = cohorte.titulo_jurisdiccional
    choices = [(i, i) for i in range(titulo_jurisdiccional.datos_cohorte.get().anio_primera_cohorte, titulo_jurisdiccional.datos_cohorte.get().anio_ultima_cohorte + 1)]
    form.fields["anio"].choices = choices

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
    current_establecimientos_ids = __flat_list(CohorteEstablecimiento.objects.filter(cohorte = cohorte).values_list("establecimiento_id"))
    current_establecimientos_oferta = __flat_list(CohorteEstablecimiento.objects.filter(cohorte = cohorte, oferta = True).values_list("establecimiento_id"))
    current_establecimientos_emite = __flat_list(CohorteEstablecimiento.objects.filter(cohorte = cohorte, emite = True).values_list("establecimiento_id"))
    #raise Exception(current_establecimientos_oferta)

    "Búsqueda de establecimientos"
    if request.method == 'GET':
        form_filters = CohorteAsignarEstablecimientosFormFilters(request.GET)
    else:
        form_filters = CohorteAsignarEstablecimientosFormFilters()

        # POST, guardo los datos
        estado = EstadoCohorteEstablecimiento.objects.get(nombre = EstadoCohorteEstablecimiento.ASIGNADA)
        values_dict = {
            'current_establecimientos_ids': current_establecimientos_ids,
            'current_oferta_ids': current_establecimientos_oferta,
            'current_emite_ids': current_establecimientos_emite,
            'post_ids': request.POST.getlist("establecimientos"),
            'post_oferta_ids': request.POST.getlist("oferta"),
            'post_emite_ids': request.POST.getlist("emite"),
            'estado': estado,
        }
        #cohorte.save_establecimientos(current_establecimientos_ids, current_establecimientos_oferta, current_establecimientos_emite, post_ids, post_oferta, post_emite, estado)
        cohorte.save_establecimientos(**values_dict)

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
        'current_establecimientos_oferta': current_establecimientos_oferta,
        'current_establecimientos_emite': current_establecimientos_emite,
        'form_filters': form_filters,
        'objects': q,
    })


def build_asignar_establecimientos_query(filters, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(ambito__path__istartswith = request.get_perfil().ambito.path)

@login_required
@credential_required('tit_cohorte_asignar')
def asignar_anexos(request, cohorte_id):

    """
    Asignar cohorte a anexos
    """

    cohorte = Cohorte.objects.get(pk = cohorte_id)
    "Traigo los ids de los anexos actualmente asignados a la cohorte"
    current_anexos_ids = __flat_list(CohorteAnexo.objects.filter(cohorte = cohorte).values_list("anexo_id"))
    current_anexos_oferta = __flat_list(CohorteAnexo.objects.filter(cohorte = cohorte, oferta = True).values_list("anexo_id"))
    current_anexos_emite = __flat_list(CohorteAnexo.objects.filter(cohorte = cohorte, emite = True).values_list("anexo_id"))

    "Búsqueda de anexos"
    if request.method == 'GET':
        form_filters = CohorteAsignarAnexosFormFilters(request.GET)
    else:
        form_filters = CohorteAsignarAnexosFormFilters()

        # POST, guardo los datos
        estado = EstadoCohorteAnexo.objects.get(nombre = EstadoCohorteAnexo.ASIGNADA)
        values_dict = {
            'current_anexos_ids': current_anexos_ids,
            'current_oferta_ids': current_anexos_oferta,
            'current_emite_ids': current_anexos_emite,
            'post_ids': request.POST.getlist("anexos"),
            'post_oferta_ids': request.POST.getlist("oferta"),
            'post_emite_ids': request.POST.getlist("emite"),
            'estado': estado,
        }
        cohorte.save_anexos(**values_dict)

        request.set_flash('success', 'Datos actualizados correctamente.')
        # redirigir a edit
        return HttpResponseRedirect(reverse('cohorteAsignarAnexos', args = [cohorte.id]))

    jurisdiccion = request.get_perfil().jurisdiccion()

    form_filters.fields["dependencia_funcional"].queryset = form_filters.fields["dependencia_funcional"].queryset.filter(jurisdiccion = jurisdiccion)
    form_filters.fields["localidad"].queryset = form_filters.fields["localidad"].queryset.filter(departamento__jurisdiccion = jurisdiccion)

    q = build_asignar_anexos_query(form_filters, request)

    return my_render(request, 'titulos/cohorte/asignar_anexos.html', {
        'cohorte': cohorte,
        'current_anexos_ids': current_anexos_ids,
        'current_anexos_oferta': current_anexos_oferta,
        'current_anexos_emite': current_anexos_emite,
        'form_filters': form_filters,
        'objects': q,
    })


def build_asignar_anexos_query(filters, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(ambito__path__istartswith = request.get_perfil().ambito.path).order_by('nombre')

@login_required
@credential_required('tit_cohorte_asignar')
def asignar_unidades_extension(request, cohorte_id):

    """
    Asignar cohorte a unidades de extensión
    """

    cohorte = Cohorte.objects.get(pk = cohorte_id)
    "Traigo los ids de los anexos actualmente asignados a la cohorte"
    current_unidades_extension_ids = __flat_list(CohorteUnidadExtension.objects.filter(cohorte = cohorte).values_list("unidad_extension_id"))
    current_unidades_extension_oferta = __flat_list(CohorteUnidadExtension.objects.filter(cohorte = cohorte, oferta = True).values_list("unidad_extension_id"))

    "Búsqueda de unidades de extensión"
    if request.method == 'GET':
        form_filters = CohorteAsignarUnidadesExtensionFormFilters(request.GET)
    else:
        form_filters = CohorteAsignarUnidadesExtensionFormFilters()

        # POST, guardo los datos
        estado = EstadoCohorteUnidadExtension.objects.get(nombre = EstadoCohorteUnidadExtension.ASIGNADA)
        values_dict = {
            'current_unidades_extension_ids': current_unidades_extension_ids,
            'current_oferta_ids': current_unidades_extension_oferta,
            'post_ids': request.POST.getlist("unidades_extension"),
            'post_oferta_ids': request.POST.getlist("oferta"),
            'estado': estado,
        }
        cohorte.save_unidades_extension(**values_dict)

        request.set_flash('success', 'Datos actualizados correctamente.')
        # redirigir a edit
        return HttpResponseRedirect(reverse('cohorteAsignarUnidadesExtension', args = [cohorte.id]))

    jurisdiccion = request.get_perfil().jurisdiccion()

    form_filters.fields["dependencia_funcional"].queryset = form_filters.fields["dependencia_funcional"].queryset.filter(jurisdiccion = jurisdiccion)
    form_filters.fields["localidad"].queryset = form_filters.fields["localidad"].queryset.filter(departamento__jurisdiccion = jurisdiccion)

    q = build_asignar_unidades_extension_query(form_filters, request)

    return my_render(request, 'titulos/cohorte/asignar_unidades_extension.html', {
        'cohorte': cohorte,
        'current_unidades_extension_ids': current_unidades_extension_ids,
        'current_unidades_extension_oferta': current_unidades_extension_oferta,
        'form_filters': form_filters,
        'objects': q,
    })


def build_asignar_unidades_extension_query(filters, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().filter(establecimiento__ambito__path__istartswith = request.get_perfil().ambito.path)


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
def __flat_list(list_to_flat):
    return [i for j in list_to_flat for i in j]

@login_required
@credential_required('revisar_jurisdiccion')
def revisar_jurisdiccion(request, oid):
    o = Cohorte.objects.get(pk = oid)
    o.revisado_jurisdiccion = True
    o.save()
    request.set_flash('success', 'Registro revisado.')
    return HttpResponseRedirect(reverse('cohortesPorTitulo', args=[o.titulo_jurisdiccional_id]))
