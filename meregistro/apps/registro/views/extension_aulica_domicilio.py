# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Localidad import Localidad
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.models.ExtensionAulicaDomicilio import ExtensionAulicaDomicilio
from apps.registro.forms.ExtensionAulicaDomicilioForm import ExtensionAulicaDomicilioForm
from apps.registro.forms.ExtensionAulicaDomicilioFormFilters import ExtensionAulicaDomicilioFormFilters
from apps.backend.models import ConfiguracionSolapasExtensionAulica
from apps.registro.forms.VerificacionDatosExtensionAulicaForm import VerificacionDatosExtensionAulicaForm

ITEMS_PER_PAGE = 50


@login_required
def __extension_aulica_dentro_del_ambito(request, extension_aulica):
    """
    El extension_aulica está dentro del ámbito?
    """
    try:
        extension_aulica = ExtensionAulica.objects.get(id=extension_aulica.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except extension_aulica.DoesNotExist:
        return False
    return True

@login_required
def __get_extension_aulica(request, extension_aulica_id):    
    extension_aulica = ExtensionAulica.objects.get(pk=extension_aulica_id)
    if not __extension_aulica_dentro_del_ambito(request, extension_aulica):
        raise Exception('El extension_aulica no se encuentra en su ámbito.')
    return extension_aulica


@login_required
@credential_required('reg_extension_aulica_modificar')
def index(request, extension_aulica_id):
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Búsqueda de extension_aulicas
    """
    if request.method == 'GET':
        form_filter = ExtensionAulicaDomicilioFormFilters(request.GET, extension_aulica_id=extension_aulica.id)
    else:
        form_filter = ExtensionAulicaFormFilters(extension_aulica_id=extension_aulica.id)
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

    return my_render(request, 'registro/extension_aulica/domicilios/index.html', {
        'extension_aulica': extension_aulica,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': extension_aulica.get_verificacion_datos().domicilios,
        'datos_verificados': extension_aulica.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasExtensionAulica.get_instance(),
        'actual_page': 'domicilios',
        'form_verificacion': VerificacionDatosExtensionAulicaForm(
			dato_verificacion='domicilios', 
			unidad_educativa_id=extension_aulica.id, 
			return_url='extensionAulicaDomiciliosIndex', 
			verificado=extension_aulica.get_verificacion_datos().domicilios),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('calle', 'altura')


@login_required
@credential_required('reg_extension_aulica_modificar')
def create(request, extension_aulica_id):
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Alta de domicilio.
    """
    jurisdiccion = extension_aulica.establecimiento.dependencia_funcional.jurisdiccion

    if request.method == 'POST':
        form = ExtensionAulicaDomicilioForm(request.POST, jurisdiccion_id=jurisdiccion.id, extension_aulica_id=extension_aulica.id)
        form.extension_aulica_id = extension_aulica_id
        if form.is_valid():
            domicilio = form.save(commit=False)
            domicilio.extension_aulica_id = extension_aulica.id
            domicilio.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaDomiciliosIndex', args=[domicilio.extension_aulica_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = ExtensionAulicaDomicilioForm(jurisdiccion_id=jurisdiccion.id, extension_aulica_id=extension_aulica.id)
    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)
    return my_render(request, 'registro/extension_aulica/domicilios/new.html', {
        'extension_aulica': extension_aulica,
        'form': form,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def edit(request, domicilio_id):
    """
    Edición de los datos de una domicilio.
    """
    domicilio = ExtensionAulicaDomicilio.objects.get(pk=domicilio_id)
    extension_aulica = __get_extension_aulica(request, domicilio.extension_aulica_id)
    jurisdiccion = extension_aulica.establecimiento.dependencia_funcional.jurisdiccion

    if request.method == 'POST':
        form = ExtensionAulicaDomicilioForm(request.POST, instance=domicilio, jurisdiccion_id=jurisdiccion.id, extension_aulica_id=extension_aulica.id)
        if form.is_valid():
            domicilio = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaDomiciliosIndex', args=[domicilio.extension_aulica_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaDomicilioForm(instance=domicilio, jurisdiccion_id=jurisdiccion.id, extension_aulica_id=extension_aulica.id)

    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)
    try:        
        localidad_seleccionada = request.POST['localidad']
    except KeyError:
        localidad_seleccionada = None
    return my_render(request, 'registro/extension_aulica/domicilios/edit.html', {
        'form': form,
        'domicilio': domicilio,
        'extension_aulica': extension_aulica,
        'localidad_seleccionada': localidad_seleccionada,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def delete(request, domicilio_id):
    domicilio = ExtensionAulicaDomicilio.objects.get(pk=domicilio_id)
    extension_aulica = __get_extension_aulica(request, domicilio.extension_aulica_id)
    
    domicilio.delete()
    request.set_flash('success', 'Datos del domicilio eliminados correctamente.')
    return HttpResponseRedirect(reverse('extensionAulicaDomiciliosIndex', args=[domicilio.extension_aulica_id]))
