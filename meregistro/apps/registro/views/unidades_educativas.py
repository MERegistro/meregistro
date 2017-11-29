# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.DependenciaFuncional import DependenciaFuncional
from apps.registro.forms.UnidadesEducativasFormFilters import UnidadesEducativasFormFilters
from django.core.paginator import Paginator
from apps.registro.FSM import FSMEstablecimiento
from apps.reportes.views.establecimiento import establecimientos as reporte_establecimientos
from apps.reportes.models import Reporte
from django.contrib import messages
from itertools import chain

fsmEstablecimiento = FSMEstablecimiento()

ITEMS_PER_PAGE = 50

def __puede_verificar_datos(request):
    return request.has_credencial('reg_establecimiento_verificar_datos')

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
@credential_required('reg_establecimiento_consulta')
def index(request):

    jurisdiccion = request.get_perfil().jurisdiccion()

    if jurisdiccion is not None:  # el usuario puede ser un referente o el admin de títulos
        jurisdiccion_id = jurisdiccion.id
    else:
        try:
            jurisdiccion_id = request.GET['jurisdiccion']
            if request.GET['jurisdiccion'] == '':
                jurisdiccion_id = None
        except KeyError:
            jurisdiccion_id = None

    try:
        departamento_id = request.GET['departamento']
        if request.GET['departamento'] == '':
            departamento_id = None
    except KeyError:
        departamento_id = None

    """
    Búsqueda de establecimientos
    """
    if request.method == 'GET':
        form_filter = UnidadesEducativasFormFilters(request.GET, jurisdiccion_id=jurisdiccion_id, departamento_id=departamento_id)
    else:
        form_filter = UnidadesEducativasFormFilters(jurisdiccion_id=jurisdiccion_id, departamento_id=departamento_id)
    q = build_query(form_filter, 1, request)

    try:
        if request.GET['export'] == '1':
            return reporte_establecimientos(request, q)
    except KeyError:
        pass

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

    if jurisdiccion is not None:
        form_filter.fields['dependencia_funcional'].queryset = DependenciaFuncional.objects.filter(jurisdiccion=jurisdiccion)
    page = paginator.page(page_number)
    objects = page.object_list
    return my_render(request, 'registro/unidades_educativas/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'export_url': Reporte.build_export_url(request.build_absolute_uri()),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    unidades_educativas = filters.buildQuery()
    sedes = unidades_educativas['sedes'].filter(ambito__path__istartswith=request.get_perfil().ambito.path)
    anexos = unidades_educativas['anexos'].order_by('establecimiento__nombre', 'cue').filter(ambito__path__istartswith=request.get_perfil().ambito.path)
    extensiones_aulicas = unidades_educativas['extensiones_aulicas'].filter(ambito__path__istartswith=request.get_perfil().ambito.path)


    unidades_educativas = [ue for ue in list(chain(sedes, anexos, extensiones_aulicas))]
    return unidades_educativas
