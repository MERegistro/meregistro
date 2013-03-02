# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.models.ExtensionAulicaAutoridad import ExtensionAulicaAutoridad
from apps.registro.forms.ExtensionAulicaAutoridadForm import ExtensionAulicaAutoridadForm
from apps.registro.forms.ExtensionAulicaAutoridadFormFilters import ExtensionAulicaAutoridadFormFilters
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
    Búsqueda de extensiones
    """
    if request.method == 'GET':
        form_filter = ExtensionAulicaAutoridadFormFilters(request.GET, extension_aulica_id=extension_aulica.id)
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

    alta_habilitada = objects.count() == 0

    return my_render(request, 'registro/extension_aulica/autoridades/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'extension_aulica': extension_aulica,
        'alta_habilitada': alta_habilitada,
        'verificado': extension_aulica.get_verificacion_datos().autoridades,
        'datos_verificados': extension_aulica.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasExtensionAulica.get_instance(),
        'current_page': 'autoridades',
        'form_verificacion': VerificacionDatosExtensionAulicaForm(
			dato_verificacion='autoridades', 
			unidad_educativa_id=extension_aulica.id, 
			return_url='extensionAulicaAutoridadesIndex', 
			verificado=extension_aulica.get_verificacion_datos().autoridades),
    })
   

def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery()


@login_required
@credential_required('reg_extension_aulica_modificar')
def create(request, extension_aulica_id):
    
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Alta de autoridad.
    """

    if request.method == 'POST':
        form = ExtensionAulicaAutoridadForm(request.POST)
        if form.is_valid():
            autoridad = form.save(commit=False)
            autoridad.extension_aulica_id = extension_aulica.id
            autoridad.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaAutoridadEdit', args=[autoridad.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = ExtensionAulicaAutoridadForm()

    # Chequear si se puede dar de alta
    # XXX: sólo se puede dar de alta un registro por ahora
    alta_habilitada = ExtensionAulicaAutoridad.objects.filter(extension_aulica__id = extension_aulica.id).count() == 0    
    if not alta_habilitada:  # no debería estar en esta pantalla
        request.set_flash('warning', 'No puede dar de alta más de una autoridad.')
        return HttpResponseRedirect(reverse('extensionAulicaAutoridadesIndex', args=[extension_aulica.id]))
    
    return my_render(request, 'registro/extension_aulica/autoridades/new.html', {
        'form': form,
        'extension_aulica': extension_aulica,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def edit(request, autoridad_id):
    """
    Edición de los datos de una autoridad.
    """    
    autoridad = ExtensionAulicaAutoridad.objects.get(pk=autoridad_id)
    extension_aulica = __get_extension_aulica(request, autoridad.extension_aulica_id)

    if request.method == 'POST':
        form = ExtensionAulicaAutoridadForm(request.POST, instance=autoridad)
        if form.is_valid():
            autoridad = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaAutoridadForm(instance=autoridad)

    return my_render(request, 'registro/extension_aulica/autoridades/edit.html', {
        'form': form,
        'autoridad': autoridad,
        'extension_aulica': extension_aulica,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def delete(request, autoridad_id):
    autoridad = ExtensionAulicaAutoridad.objects.get(pk=autoridad_id)
    extension_aulica = __get_extension_aulica(request, autoridad.extension_aulica_id)
    autoridad.delete()
    request.set_flash('success', 'Datos de la autoridad eliminados correctamente.')
    return HttpResponseRedirect(reverse('extensionAulicaAutoridadesIndex', args=[extension_aulica.id]))
