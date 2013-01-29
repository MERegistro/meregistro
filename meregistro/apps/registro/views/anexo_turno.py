# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Anexo import Anexo
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.AnexoTurno import AnexoTurno
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.forms.AnexoTurnoForm import AnexoTurnoForm
from apps.registro.forms.AnexoTurnoFormFilters import AnexoTurnoFormFilters
from apps.backend.models import ConfiguracionSolapasAnexo

ITEMS_PER_PAGE = 50

@login_required
def __anexo_dentro_del_ambito(request, anexo):
    """
    La sede está dentro del ámbito?
    """
    try:
        anexo = Anexo.objects.get(id=anexo.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except anexo.DoesNotExist:
        return False
    return True


@login_required
def __get_anexo(request, anexo_id):
    
    anexo = Anexo.objects.get(pk=anexo_id)

    if not __anexo_dentro_del_ambito(request, anexo):
        raise Exception('La sede no se encuentra en su ámbito.')

    if anexo.estado.nombre == EstadoAnexo.PENDIENTE:
        if 'reg_editar_anexo_pendiente' not in request.get_credenciales():
            raise Exception('Usted no tiene permisos para editar los datos del anexo pendiente')

    return anexo


@login_required
#@credential_required('reg_anexo_ver')
def index(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    Búsqueda de anexos
    """
    if request.method == 'GET':
        form_filter = AnexoTurnoFormFilters(request.GET, anexo_id=anexo.id)
    else:
        form_filter = AnexoTurnoFormFilters(anexo_id=anexo.id)
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
    
    if not anexo.get_verificacion_datos().completo():
        request.set_flash('warning', 'Las solapas cuyos datos todavía no han sido verificados se verán en color rojo. Por favor, verifique los datos.')
		    
    return my_render(request, 'registro/anexo/turnos/index.html', {
        'anexo': anexo,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': anexo.get_verificacion_datos().turnos,
        'datos_verificados': anexo.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasAnexo.get_instance(),
        'actual_page': 'turnos'
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('turno__nombre')


@login_required
@credential_required('reg_anexo_completar')
def create(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    Alta de turno.
    """

    if request.method == 'POST':
        form = AnexoTurnoForm(request.POST, anexo_id=anexo.id)
        if form.is_valid():
            anexo_turno = form.save(commit=False)
            anexo_turno.anexo_id = anexo_id
            anexo_turno.save()
            form.save_m2m()
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('anexoTurnosIndex', args=[anexo_turno.anexo_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = AnexoTurnoForm(anexo_id=anexo.id)
        
    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    return my_render(request, 'registro/anexo/turnos/new.html', {
        'anexo': anexo,
        'form': form,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
    })


@login_required
@credential_required('reg_anexo_completar')
def edit(request, anexo_turno_id):
    """
    Edición de los datos de un turno.
    """
    anexo_turno = AnexoTurno.objects.get(pk=anexo_turno_id)
    anexo = __get_anexo(request, anexo_turno.anexo_id)

    if request.method == 'POST':
        form = AnexoTurnoForm(request.POST, instance=anexo_turno, anexo_id=anexo.id)
        if form.is_valid():
            anexo_turno = form.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('anexoTurnosIndex', args=[anexo_turno.anexo_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoTurnoForm(instance=anexo_turno, anexo_id=anexo.id)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    return my_render(request, 'registro/anexo/turnos/edit.html', {
        'form': form,
        'anexo_turno': anexo_turno,
        'anexo': anexo,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
    })


@login_required
@credential_required('reg_anexo_completar')
def delete(request, anexo_turno_id):
    anexo_turno = AnexoTurno.objects.get(pk=anexo_turno_id)
    anexo = __get_anexo(request, anexo_turno.anexo_id)
    
    anexo_turno.delete()
    request.set_flash('success', 'Datos del turno eliminados correctamente.')
    return HttpResponseRedirect(reverse('anexoTurnosIndex', args=[anexo_turno.anexo_id]))
