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
from apps.registro.models.EstablecimientoAutoridad import EstablecimientoAutoridad
from apps.registro.forms.EstablecimientoAutoridadForm import EstablecimientoAutoridadForm
from apps.registro.forms.EstablecimientoAutoridadFormFilters import EstablecimientoAutoridadFormFilters
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
@credential_required('reg_establecimiento_ver')
def index(request, establecimiento_id):
    
    establecimiento = __get_establecimiento(request, establecimiento_id)

    return HttpResponseRedirect(reverse('establecimientoCompletarContacto', args=[establecimiento.id]))
    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = EstablecimientoAutoridadFormFilters(request.GET, establecimiento_id=establecimiento.id)
    else:
        form_filter = EstablecimientoAutoridadFormFilters(establecimiento_id=establecimiento.id)

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

    alta_habilitada = objects.count() == 0
    
    return my_render(request, 'registro/establecimiento/autoridades/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'establecimiento': establecimiento,
        'alta_habilitada': alta_habilitada,
        'verificado': establecimiento.get_verificacion_datos().autoridades,
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'actual_page': 'contacto',
        'form_verificacion': VerificacionDatosEstablecimientoForm(
			dato_verificacion='autoridades', 
			unidad_educativa_id=establecimiento.id, 
			return_url='establecimientoAutoridadesIndex', 
			verificado=establecimiento.get_verificacion_datos().autoridades),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery()


@login_required
@credential_required('reg_establecimiento_completar')
def create(request, establecimiento_id):
    
    establecimiento = __get_establecimiento(request, establecimiento_id)
    """
    Alta de autoridad.
    """

    if request.method == 'POST':
        form = EstablecimientoAutoridadForm(request.POST)
        if form.is_valid():
            autoridad = form.save(commit=False)
            autoridad.establecimiento_id = establecimiento.id
            autoridad.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoAutoridadEdit', args=[autoridad.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoAutoridadForm()

    # Chequear si se puede dar de alta
    # XXX: sólo se puede dar de alta un registro por ahora
    # Se habilita el 29.11.2017
    #alta_habilitada = EstablecimientoAutoridad.objects.filter(establecimiento__id = establecimiento.id).count() == 0    
    #if not alta_habilitada:  # no debería estar en esta pantalla
    #    request.set_flash('warning', 'No puede dar de alta más de una autoridad.')
    #    return HttpResponseRedirect(reverse('establecimientoCompletarContacto', args=[establecimiento.id]))
    
    return my_render(request, 'registro/establecimiento/autoridades/new.html', {
        'form': form,
        'establecimiento': establecimiento,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def edit(request, autoridad_id):
    """
    Edición de los datos de una autoridad.
    """    
    autoridad = EstablecimientoAutoridad.objects.get(pk=autoridad_id)
    establecimiento = __get_establecimiento(request, autoridad.establecimiento_id)

    if request.method == 'POST':
        form = EstablecimientoAutoridadForm(request.POST, instance=autoridad)
        if form.is_valid():
            autoridad = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoAutoridadForm(instance=autoridad)

    return my_render(request, 'registro/establecimiento/autoridades/edit.html', {
        'form': form,
        'autoridad': autoridad,
        'establecimiento': establecimiento,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def delete(request, autoridad_id):
    autoridad = EstablecimientoAutoridad.objects.get(pk=autoridad_id)
    establecimiento = __get_establecimiento(request, autoridad.establecimiento_id)
    autoridad.delete()
    request.set_flash('success', 'Datos de la autoridad eliminados correctamente.')
    return HttpResponseRedirect(reverse('establecimientoCompletarContacto', args=[establecimiento.id]))
    #return HttpResponseRedirect(reverse('establecimientoAutoridadesIndex', args=[establecimiento.id]))
