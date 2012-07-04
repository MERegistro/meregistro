# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.titulos.models import TituloJurisdiccional, EgresadosEstablecimiento, EstadoTituloJurisdiccional, EgresadosEstablecimientoDetalle
from apps.titulos.forms import EgresadosEstablecimientoForm, EgresadosEstablecimientoDetalleForm, EgresadosEstablecimientoFormFilters
from apps.registro.models import Establecimiento, Anexo
from django.core.paginator import Paginator
import datetime

ITEMS_PER_PAGE = 50


def __get_establecimiento_actual(request):
    """
    Trae el único establecimiento que tiene asignado, por ejemplo, un rector/director
    """
    try:
        return Establecimiento.objects.get(ambito__id=request.get_perfil().ambito.id)
    except Establecimiento.DoesNotExist:
		raise Exception('ERROR: El usuario no tiene asignado un establecimiento.')


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    establecimiento = __get_establecimiento_actual(request)
    estado = EstadoTituloJurisdiccional.objects.get(nombre=EstadoTituloJurisdiccional.CONTROLADO)
    # Traer los títulos que tengan cohortes asignadas en este establecimiento
    return filters.buildQuery().filter(cohortes__cohorteestablecimiento__establecimiento=establecimiento, estado__nombre=estado).order_by('titulo__nombre')


@login_required
#@credential_required('tit_egresados_establecimiento')
def index(request):
    """
    Index de egresados
    """
    establecimiento = __get_establecimiento_actual(request)

    if request.method == 'GET':
        form_filter = EgresadosEstablecimientoFormFilters(request.GET)
    else:
        form_filter = EgresadosEstablecimientoFormFilters()
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
    return my_render(request, 'titulos/egresados_establecimiento/index.html', {
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
#@credential_required('tit_egresados_establecimiento')
def egresados_por_titulo(request, titulo_jurisdiccional_id):

    establecimiento = __get_establecimiento_actual(request)
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)
    objects = EgresadosEstablecimiento.objects.filter(titulo_jurisdiccional=titulo_jurisdiccional_id, establecimiento=establecimiento)

    return my_render(request, 'titulos/egresados_establecimiento/egresados_por_titulo.html', {
        'objects': objects,
        'titulo_jurisdiccional': titulo_jurisdiccional
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def create(request, titulo_jurisdiccional_id):
    """
    Alta de egresados en establecimiento.
    """
    establecimiento = __get_establecimiento_actual(request)
    titulo_jurisdiccional = TituloJurisdiccional.objects.get(pk=titulo_jurisdiccional_id)

    if request.method == 'POST':
        form = EgresadosEstablecimientoForm(request.POST, establecimiento_id=establecimiento.id, titulo_jurisdiccional_id=titulo_jurisdiccional.id)
        if form.is_valid():
            egresados = form.save(commit=False)
            egresados.establecimiento = establecimiento
            egresados.titulo_jurisdiccional = titulo_jurisdiccional
            egresados.save()
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('establecimientoEgresadosPorTitulo', args=[titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EgresadosEstablecimientoForm(establecimiento_id=establecimiento.id, titulo_jurisdiccional_id=titulo_jurisdiccional.id)

    return my_render(request, 'titulos/egresados_establecimiento/new.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': True,
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def edit(request, egresados_establecimiento_id):
    """
    Edición de egresados.
    """
    egresados = EgresadosEstablecimiento.objects.get(pk=egresados_establecimiento_id)
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        form = EgresadosEstablecimientoForm(request.POST, instance=egresados, establecimiento_id=egresados.establecimiento_id, titulo_jurisdiccional_id=egresados.titulo_jurisdiccional_id)
        if form.is_valid():
            egresados = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoEgresadosPorTitulo', args=[titulo_jurisdiccional.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EgresadosEstablecimientoForm(instance=egresados, establecimiento_id=egresados.establecimiento_id, titulo_jurisdiccional_id=egresados.titulo_jurisdiccional_id)

    return my_render(request, 'titulos/egresados_establecimiento/edit.html', {
        'form': form,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': False,
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def eliminar(request, egresados_establecimiento_id):
    """
    Baja de un dato de egresados
    """
    egresados = EgresadosEstablecimiento.objects.get(pk=egresados_establecimiento_id)
    titulo_jurisdiccional_id = egresados.titulo_jurisdiccional_id

    if request.method == 'POST':
        if int(request.POST['egresados_establecimiento_id']) is not int(egresados.id):
            raise Exception('Error en la consulta!')

        egresados.delete()
        request.set_flash('success', 'El registro fue dado de baja correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('establecimientoEgresadosPorTitulo', args=[titulo_jurisdiccional_id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el registro? Esta operación no puede deshacerse.')

    return my_render(request, 'titulos/egresados_establecimiento/eliminar.html', {
        'egresados_id': egresados.id,
        'titulo_jurisdiccional_id': titulo_jurisdiccional_id,
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def detalle(request, egresados_establecimiento_id):

    egresados = EgresadosEstablecimiento.objects.get(pk=egresados_establecimiento_id)

    objects = EgresadosEstablecimientoDetalle.objects.filter(egresados_establecimiento=egresados.id)

    return my_render(request, 'titulos/egresados_establecimiento/detalle.html', {
        'objects': objects,
        'egresados': egresados,
        'titulo_jurisdiccional': egresados.titulo_jurisdiccional,
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def agregar_detalle(request, egresados_establecimiento_id):
    """
    Agregar detalles de egresados en establecimiento.
    """
    establecimiento = __get_establecimiento_actual(request)
    egresados = EgresadosEstablecimiento.objects.get(pk=egresados_establecimiento_id)
    titulo_jurisdiccional = egresados.titulo_jurisdiccional
    
    if request.method == 'POST':
        form = EgresadosEstablecimientoDetalleForm(request.POST, egresados_establecimiento_id=egresados.id, max_egresados=egresados.cantidad_egresados)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.egresados_establecimiento = egresados
            detalle.save()
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir a edit
            return HttpResponseRedirect(reverse('establecimientoEgresadosDetalle', args=[egresados.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EgresadosEstablecimientoDetalleForm(egresados_establecimiento_id=egresados.id, max_egresados=egresados.cantidad_egresados)

    return my_render(request, 'titulos/egresados_establecimiento/new_detalle.html', {
        'form': form,
        'egresados': egresados,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': False,
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def edit_detalle(request, detalle_id):
    """
    Edición de detalle de egresados.
    """
    detalle = EgresadosEstablecimientoDetalle.objects.get(pk=detalle_id)
    egresados = detalle.egresados_establecimiento
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        form = EgresadosEstablecimientoDetalleForm(request.POST, instance=detalle, egresados_establecimiento_id=egresados.id, max_egresados=egresados.cantidad_egresados)
        if form.is_valid():
            detalle = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoEgresadosDetalle', args=[egresados.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EgresadosEstablecimientoDetalleForm(instance=detalle, egresados_establecimiento_id=egresados.id, max_egresados=egresados.cantidad_egresados)

    return my_render(request, 'titulos/egresados_establecimiento/edit_detalle.html', {
        'form': form,
        'detalle': detalle,
        'egresados': egresados,
        'titulo_jurisdiccional': titulo_jurisdiccional,
        'is_new': False,
    })


@login_required
#@credential_required('tit_egresados_establecimiento')
def eliminar_detalle(request, detalle_id):
    """
    Baja de un dato de detalle de egresados
    """
    detalle = EgresadosEstablecimientoDetalle.objects.get(pk=detalle_id)
    egresados = detalle.egresados_establecimiento
    titulo_jurisdiccional = egresados.titulo_jurisdiccional

    if request.method == 'POST':
        if int(request.POST['egresados_establecimiento_detalle_id']) is not int(detalle.id):
            raise Exception('Error en la consulta!')

        detalle.delete()
        request.set_flash('success', 'El registro fue dado de baja correctamente.')
        """ Redirecciono para evitar el reenvío del form """
        return HttpResponseRedirect(reverse('establecimientoEgresadosDetalle', args=[egresados.id]))
    else:
        request.set_flash('warning', 'Está seguro de eliminar el detalle? Esta operación no puede deshacerse.')
    return my_render(request, 'titulos/egresados_establecimiento/eliminar_detalle.html', {
        'detalle': detalle,
        'egresados': egresados,
        'titulo_jurisdiccional': titulo_jurisdiccional,
    })
