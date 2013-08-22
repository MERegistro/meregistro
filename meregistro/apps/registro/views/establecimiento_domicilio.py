# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Localidad import Localidad
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.EstablecimientoDomicilio import EstablecimientoDomicilio
from apps.registro.forms.EstablecimientoDomicilioForm import EstablecimientoDomicilioForm
from apps.registro.forms.EstablecimientoDomicilioFormFilters import EstablecimientoDomicilioFormFilters
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
    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = EstablecimientoDomicilioFormFilters(request.GET, establecimiento_id=establecimiento.id)
    else:
        form_filter = EstablecimientoDomicilioFormFilters(establecimiento_id=establecimiento.id)
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
    
    return my_render(request, 'registro/establecimiento/domicilios/index.html', {
        'establecimiento': establecimiento,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': establecimiento.get_verificacion_datos().domicilios,
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'actual_page': 'domicilios',
        'form_verificacion': VerificacionDatosEstablecimientoForm(
			dato_verificacion='domicilios', 
			unidad_educativa_id=establecimiento.id, 
			return_url='establecimientoDomiciliosIndex', 
			verificado=establecimiento.get_verificacion_datos().domicilios),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('calle', 'altura')


@login_required
@credential_required('reg_establecimiento_completar')
def create(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    """
    Alta de domicilio.
    """
    jurisdiccion = establecimiento.dependencia_funcional.jurisdiccion

    if request.method == 'POST':
        form = EstablecimientoDomicilioForm(request.POST, jurisdiccion_id=jurisdiccion.id, establecimiento_id=establecimiento.id)
        if form.is_valid():
            domicilio = form.save(commit=False)
            domicilio.establecimiento_id = establecimiento.id
            domicilio.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoDomiciliosIndex', args=[domicilio.establecimiento_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoDomicilioForm(jurisdiccion_id=jurisdiccion.id, establecimiento_id=establecimiento.id)
    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)
    "Localidad seleccionada al hacer refresh"
    try:        
        localidad_seleccionada = request.POST['localidad']
    except KeyError:
        localidad_seleccionada = None
    return my_render(request, 'registro/establecimiento/domicilios/new.html', {
        'establecimiento': establecimiento,
        'form': form,
        'localidad_seleccionada': localidad_seleccionada,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def edit(request, domicilio_id):
    """
    Edición de los datos de una domicilio.
    """
    domicilio = EstablecimientoDomicilio.objects.get(pk=domicilio_id)
    establecimiento = __get_establecimiento(request, domicilio.establecimiento_id)
    jurisdiccion = establecimiento.dependencia_funcional.jurisdiccion

    if request.method == 'POST':
        form = EstablecimientoDomicilioForm(request.POST, instance=domicilio, jurisdiccion_id=jurisdiccion.id, establecimiento_id=establecimiento.id)
        if form.is_valid():
            domicilio = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoDomiciliosIndex', args=[domicilio.establecimiento_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoDomicilioForm(instance=domicilio, jurisdiccion_id=jurisdiccion.id, establecimiento_id=establecimiento.id)

    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)
    return my_render(request, 'registro/establecimiento/domicilios/edit.html', {
        'form': form,
        'domicilio': domicilio,
        'establecimiento': establecimiento,
    })


@login_required
@credential_required('reg_establecimiento_completar')
def delete(request, domicilio_id):
    domicilio = EstablecimientoDomicilio.objects.get(pk=domicilio_id)
    establecimiento = __get_establecimiento(request, domicilio.establecimiento_id)
    
    domicilio.delete()
    request.set_flash('success', 'Datos del domicilio eliminados correctamente.')
    return HttpResponseRedirect(reverse('establecimientoDomiciliosIndex', args=[domicilio.establecimiento_id]))
