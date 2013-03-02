# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.EstablecimientoMatricula import EstablecimientoMatricula
from apps.registro.forms.EstablecimientoMatriculaForm import EstablecimientoMatriculaForm
from apps.registro.forms.EstablecimientoMatriculaFormFilters import EstablecimientoMatriculaFormFilters
from apps.backend.models import ConfiguracionSolapasEstablecimiento
from apps.registro.forms.VerificacionDatosEstablecimientoForm import VerificacionDatosEstablecimientoForm

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
        form_filter = EstablecimientoMatriculaFormFilters(request.GET, establecimiento_id=establecimiento.id)
    else:
        form_filter = EstablecimientoMatriculaFormFilters(establecimiento_id=establecimiento.id)
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

    return my_render(request, 'registro/establecimiento/matricula/index.html', {
        'establecimiento': establecimiento,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': establecimiento.get_verificacion_datos().matricula,
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'current_page': 'matricula',
        'form_verificacion': VerificacionDatosEstablecimientoForm(
			dato_verificacion='matricula',
			unidad_educativa_id=establecimiento.id,
			return_url='establecimientoMatriculaIndex',
			verificado=establecimiento.get_verificacion_datos().matricula),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('anio')


@login_required
@credential_required('reg_establecimiento_completar')
def create(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    """
    Alta de matricula.
    """

    if request.method == 'POST':
        form = EstablecimientoMatriculaForm(request.POST, establecimiento=establecimiento)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.establecimiento_id = establecimiento.id
            matricula.set_formacion_continua()
            matricula.set_formacion_docente()
            matricula.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoMatriculaIndex', args=[matricula.establecimiento_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoMatriculaForm(establecimiento=establecimiento)
    return my_render(request, 'registro/establecimiento/matricula/new.html', {
        'establecimiento': establecimiento,
        'form': form,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def edit(request, matricula_id):
    """
    Edición de los datos de una matricula.
    """
    matricula = EstablecimientoMatricula.objects.get(pk=matricula_id)
    establecimiento = __get_establecimiento(request, matricula.establecimiento_id)

    if request.method == 'POST':
        form = EstablecimientoMatriculaForm(request.POST, instance=matricula, establecimiento=establecimiento)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.set_formacion_continua()
            matricula.set_formacion_docente()
            matricula.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoMatriculaIndex', args=[matricula.establecimiento_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoMatriculaForm(instance=matricula, establecimiento=establecimiento)

    return my_render(request, 'registro/establecimiento/matricula/edit.html', {
        'form': form,
        'matricula': matricula,
        'establecimiento': establecimiento,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def delete(request, matricula_id):
    matricula = EstablecimientoMatricula.objects.get(pk=matricula_id)
    establecimiento = __get_establecimiento(request, matricula.establecimiento_id)
    matricula.delete()
    request.set_flash('success', 'Datos del matricula eliminados correctamente.')
    return HttpResponseRedirect(reverse('establecimientoMatriculaIndex', args=[matricula.establecimiento_id]))
