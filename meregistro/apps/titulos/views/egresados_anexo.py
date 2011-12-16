# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import TituloJurisdiccional, EgresadosAnexo, EstadoTituloJurisdiccional, EgresadosAnexoDetalle
from apps.titulos.forms import EgresadosAnexoForm, EgresadosAnexoDetalleForm, EgresadosAnexoFormFilters
from apps.registro.models import Anexo
from django.core.paginator import Paginator
import datetime

ITEMS_PER_PAGE = 50


def __get_anexo_actual(request):
    """
    Trae el único anexo que tiene asignado el usuario anexo
    """
    try:
        anexo = Anexo.objects.get(ambito__id = request.get_perfil().ambito.id)
        if not bool(anexo):
            raise Exception('ERROR: El usuario no tiene asignado un anexo.')
        else:
            return anexo
    except Exception:
        pass


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    anexo = __get_anexo_actual(request)
    estado = EstadoTituloJurisdiccional.objects.get(nombre = EstadoTituloJurisdiccional.CONTROLADO)
    # Traer los títulos que tengan cohortes asignadas en este anexo
    return filters.buildQuery().filter(cohortes__cohorteanexo__anexo = anexo, estado__nombre = estado).order_by('titulo__nombre')

@login_required
@credential_required('tit_egresados_anexo')
def index(request):
    """
    Index de egresados
    """
    anexo = __get_anexo_actual(request)

    if request.method == 'GET':
        form_filter = EgresadosAnexoFormFilters(request.GET)
    else:
        form_filter = EgresadosAnexoFormFilters()
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
    return my_render(request, 'titulos/egresados_anexo/index.html', {
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
@credential_required('tit_egresados_anexo')
def egresados_por_titulo(request, titulo_jurisdiccional_id):

    anexo = __get_anexo_actual(request)
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)
    objects = EgresadosAnexo.objects.filter(titulo_jurisdiccional = titulo_jurisdiccional_id, anexo = anexo)

    return my_render(request, 'titulos/egresados_anexo/egresados_por_titulo.html', {
        'objects': objects,
        'titulo_jurisdiccional': titulo_jurisdiccional
    })


@login_required
@credential_required('tit_egresados_anexo')
def create(request, titulo_jurisdiccional_id):
    """
    Alta de egresados en anexo.
    """
    anexo = __get_anexo_actual(request)

    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk = titulo_jurisdiccional_id)

    if request.method == 'POST':
        form = EgresadosAnexoForm(request.POST, anexo_id = anexo.id, titulo_jurisdiccional_id = titulo_jurisdiccional.id)
        if form.is_valid():
            egresados = form.save(commit = False)
            egresados.anexo = anexo
            egresados.titulo_jurisdiccional = titulo_jurisdiccional
            egresados.save()
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('anexoEgresadosPorTitulo', args = [titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EgresadosAnexoForm(anexo_id = anexo.id, titulo_jurisdiccional_id = titulo_jurisdiccional.id)

    return my_render(request, 'titulos/egresados_anexo/new.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': True,
    })


@login_required
@credential_required('tit_egresados_anexo')
def edit(request, egresados_anexo_id):
    """
    Edición de egresados.
    """
    egresados = EgresadosAnexo.objects.get(pk = egresados_anexo_id)
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        form = EgresadosAnexoForm(request.POST, instance = egresados, anexo_id = egresados.anexo_id, titulo_jurisdiccional_id = egresados.titulo_jurisdiccional_id)
        if form.is_valid():
            egresados = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('anexoEgresadosPorTitulo', args = [titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EgresadosAnexoForm(instance = egresados, anexo_id = egresados.anexo_id, titulo_jurisdiccional_id = egresados.titulo_jurisdiccional_id)

    return my_render(request, 'titulos/egresados_anexo/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': False,
    })


@login_required
@credential_required('tit_egresados_anexo')
def eliminar(request, egresados_anexo_id):
    """
    Baja de un dato de egresados
    """
    egresados = EgresadosAnexo.objects.get(pk = egresados_anexo_id)
    titulo_jurisdiccional_id = egresados.titulo_jurisdiccional_id

    if request.method == 'POST':
        if int(request.POST['egresados_anexo_id']) is not int(egresados.id):
            raise Exception('Error en la consulta!')

        egresados.delete()
        request.set_flash('success', 'El registro fue dado de baja correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('anexoEgresadosPorTitulo', args = [titulo_jurisdiccional_id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el registro? Esta operación no puede deshacerse.')

    return my_render(request, 'titulos/egresados_anexo/eliminar.html', {
        'egresados_id': egresados.id,
        'titulo_jurisdiccional_id': titulo_jurisdiccional_id,
    })


@login_required
@credential_required('tit_egresados_anexo')
def detalle(request, egresados_anexo_id):

    egresados = EgresadosAnexo.objects.get(pk = egresados_anexo_id)

    objects = EgresadosAnexoDetalle.objects.filter(egresados_anexo = egresados.id)

    return my_render(request, 'titulos/egresados_anexo/detalle.html', {
        'objects': objects,
        'egresados': egresados,
        'titulo_jurisdiccional': egresados.titulo_jurisdiccional,
    })


@login_required
@credential_required('tit_egresados_anexo')
def agregar_detalle(request, egresados_anexo_id):
    """
    Agregar detalles de egresados en anexo.
    """
    anexo = __get_anexo_actual(request)
    egresados = EgresadosAnexo.objects.get(pk = egresados_anexo_id)
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        form = EgresadosAnexoDetalleForm(request.POST, egresados_anexo_id = egresados.id, max_egresados = egresados.cantidad_egresados)
        if form.is_valid():
            detalle = form.save(commit = False)
            detalle.egresados_anexo = egresados
            detalle.save()
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('anexoEgresadosDetalle', args = [egresados.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EgresadosAnexoDetalleForm(egresados_anexo_id = egresados.id, max_egresados = egresados.cantidad_egresados)

    return my_render(request, 'titulos/egresados_anexo/new_detalle.html', {
        'form': form,
        'egresados': egresados,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': False,
    })


@login_required
@credential_required('tit_egresados_anexo')
def edit_detalle(request, detalle_id):
    """
    Edición de detalle de egresados.
    """
    detalle = EgresadosAnexoDetalle.objects.get(pk = detalle_id)
    egresados = detalle.egresados_anexo
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        form = EgresadosAnexoDetalleForm(request.POST, instance = detalle, egresados_anexo_id = egresados.id, max_egresados = egresados.cantidad_egresados)
        if form.is_valid():
            detalle = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('anexoEgresadosDetalle', args = [egresados.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EgresadosAnexoDetalleForm(instance = detalle, egresados_anexo_id = egresados.id, max_egresados = egresados.cantidad_egresados)

    return my_render(request, 'titulos/egresados_anexo/edit_detalle.html', {
        'form': form,
        'detalle': detalle,
        'egresados': egresados,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': False,
    })


@login_required
@credential_required('tit_egresados_anexo')
def eliminar_detalle(request, detalle_id):
    """
    Baja de un dato de detalle de egresados
    """
    detalle = EgresadosAnexoDetalle.objects.get(pk = detalle_id)
    egresados = detalle.egresados_anexo
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        if int(request.POST['egresados_anexo_detalle_id']) is not int(detalle.id):
            raise Exception('Error en la consulta!')

        detalle.delete()
        request.set_flash('success', 'El registro fue dado de baja correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('anexoEgresadosDetalle', args = [egresados.id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el detalle? Esta operación no puede deshacerse.')
    return my_render(request, 'titulos/egresados_anexo/eliminar_detalle.html', {
        'detalle': detalle,
        'egresados': egresados,
        'titulo_jurisdiccional': titulo_jurisdiccional,
    })
