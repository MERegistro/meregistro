# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.ExtensionAulica import ExtensionAulica
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.ExtensionAulicaTurno import ExtensionAulicaTurno
from apps.registro.models.EstadoExtensionAulica import EstadoExtensionAulica
from apps.registro.forms.ExtensionAulicaTurnoForm import ExtensionAulicaTurnoForm
from apps.registro.forms.ExtensionAulicaTurnoFormFilters import ExtensionAulicaTurnoFormFilters
from apps.backend.models import ConfiguracionSolapasExtensionAulica

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
#@credential_required('reg_extension_aulica_ver')
def index(request, extension_aulica_id):
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Búsqueda de extension_aulicas
    """
    if request.method == 'GET':
        form_filter = ExtensionAulicaTurnoFormFilters(request.GET, extension_aulica_id=extension_aulica.id)
    else:
        form_filter = ExtensionAulicaTurnoFormFilters(extension_aulica_id=extension_aulica.id)
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
    
    if not extension_aulica.get_verificacion_datos().completo():
        request.set_flash('warning', 'Las solapas cuyos datos todavía no han sido verificados se verán en color rojo. Por favor, verifique los datos.')

    return my_render(request, 'registro/extension_aulica/turnos/index.html', {
        'extension_aulica': extension_aulica,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': extension_aulica.get_verificacion_datos().turnos,
        'datos_verificados': extension_aulica.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasExtensionAulica.get_instance(),
        'actual_page': 'turnos'
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('turno__nombre')


@login_required
@credential_required('reg_extension_aulica_modificar')
def create(request, extension_aulica_id):
    extension_aulica = __get_extension_aulica(request, extension_aulica_id)
    """
    Alta de turno.
    """

    if request.method == 'POST':
        form = ExtensionAulicaTurnoForm(request.POST, extension_aulica_id=extension_aulica.id)
        if form.is_valid():
            extension_aulica_turno = form.save(commit=False)
            extension_aulica_turno.extension_aulica_id = extension_aulica_id
            extension_aulica_turno.save()
            form.save_m2m()
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaTurnosIndex', args=[extension_aulica_turno.extension_aulica_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = ExtensionAulicaTurnoForm(extension_aulica_id=extension_aulica.id)
        
    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    return my_render(request, 'registro/extension_aulica/turnos/new.html', {
        'extension_aulica': extension_aulica,
        'form': form,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def edit(request, extension_aulica_turno_id):
    """
    Edición de los datos de un turno.
    """
    extension_aulica_turno = ExtensionAulicaTurno.objects.get(pk=extension_aulica_turno_id)
    extension_aulica = __get_extension_aulica(request, extension_aulica_turno.extension_aulica_id)

    if request.method == 'POST':
        form = ExtensionAulicaTurnoForm(request.POST, instance=extension_aulica_turno, extension_aulica_id=extension_aulica.id)
        if form.is_valid():
            extension_aulica_turno = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('extensionAulicaTurnosIndex', args=[extension_aulica_turno.extension_aulica_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = ExtensionAulicaTurnoForm(instance=extension_aulica_turno, extension_aulica_id=extension_aulica.id)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    return my_render(request, 'registro/extension_aulica/turnos/edit.html', {
        'form': form,
        'extension_aulica_turno': extension_aulica_turno,
        'extension_aulica': extension_aulica,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
    })


@login_required
@credential_required('reg_extension_aulica_modificar')
def delete(request, extension_aulica_turno_id):
    extension_aulica_turno = ExtensionAulicaTurno.objects.get(pk=extension_aulica_turno_id)
    extension_aulica = __get_extension_aulica(request, extension_aulica_turno.extension_aulica_id)
    
    extension_aulica_turno.delete()
    request.set_flash('success', 'Datos del turno eliminados correctamente.')
    return HttpResponseRedirect(reverse('extensionAulicaTurnosIndex', args=[extension_aulica_turno.extension_aulica_id]))
