# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.EstablecimientoTurno import EstablecimientoTurno
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.forms.EstablecimientoTurnoForm import EstablecimientoTurnoForm
from apps.registro.forms.EstablecimientoTurnoFormFilters import EstablecimientoTurnoFormFilters

ITEMS_PER_PAGE = 50

@login_required
def __establecimiento_dentro_del_ambito(request, establecimiento):
    """
    La sede está dentro del ámbito?
    """
    try:
        establecimiento = Establecimiento.objects.get(id=establecimiento.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except establecimiento.DoesNotExist:
        return False
    return True

@login_required
def __get_establecimiento(request, establecimiento_id):
    establecimiento = Establecimiento.objects.get(pk=establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    if establecimiento.estado.nombre == EstadoEstablecimiento.PENDIENTE:
        if 'reg_editar_establecimiento_pendiente' not in request.get_credenciales():
            raise Exception('Usted no tiene permisos para editar los datos del establecimiento pendiente')

    return establecimiento

@login_required
@credential_required('reg_establecimiento_completar')
def index(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = EstablecimientoTurnoFormFilters(request.GET, establecimiento_id=establecimiento.id)
    else:
        form_filter = EstablecimientoTurnoFormFilters(establecimiento_id=establecimiento.id)
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
    return my_render(request, 'registro/establecimiento/turnos/index.html', {
        'establecimiento': establecimiento,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': establecimiento.get_verificacion_datos().turnos
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('turno__nombre')


@login_required
@credential_required('reg_establecimiento_completar')
def create(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    """
    Alta de turno.
    """

    if request.method == 'POST':
        form = EstablecimientoTurnoForm(request.POST, establecimiento_id=establecimiento.id)
        if form.is_valid():
            establecimiento_turno = form.save(commit=False)
            establecimiento_turno.establecimiento_id = establecimiento_id
            establecimiento_turno.save()
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoTurnosIndex', args=[establecimiento_turno.establecimiento_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoTurnoForm(establecimiento_id=establecimiento.id)
        
    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    return my_render(request, 'registro/establecimiento/turnos/new.html', {
        'establecimiento': establecimiento,
        'form': form,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def edit(request, establecimiento_turno_id):
    """
    Edición de los datos de un turno.
    """
    establecimiento_turno = EstablecimientoTurno.objects.get(pk=establecimiento_turno_id)
    establecimiento = __get_establecimiento(request, establecimiento_turno.establecimiento_id)

    if request.method == 'POST':
        form = EstablecimientoTurnoForm(request.POST, instance=establecimiento_turno, establecimiento_id=establecimiento.id)
        if form.is_valid():
            establecimiento_turno = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoTurnosIndex', args=[establecimiento_turno.establecimiento_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoTurnoForm(instance=establecimiento_turno, establecimiento_id=establecimiento.id)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    return my_render(request, 'registro/establecimiento/turnos/edit.html', {
        'form': form,
        'establecimiento_turno': establecimiento_turno,
        'establecimiento': establecimiento,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def delete(request, establecimiento_turno_id):
    establecimiento_turno = EstablecimientoTurno.objects.get(pk=establecimiento_turno_id)
    establecimiento = __get_establecimiento(request, establecimiento_turno.establecimiento_id)
    
    establecimiento_turno.delete()
    request.set_flash('success', 'Datos del turno eliminados correctamente.')
    return HttpResponseRedirect(reverse('establecimientoTurnosIndex', args=[establecimiento_turno.establecimiento_id]))
