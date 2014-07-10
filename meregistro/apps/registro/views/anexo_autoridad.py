# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Anexo import Anexo
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.models.AnexoAutoridad import AnexoAutoridad
from apps.registro.forms.AnexoAutoridadForm import AnexoAutoridadForm
from apps.registro.forms.AnexoAutoridadFormFilters import AnexoAutoridadFormFilters
from apps.backend.models import ConfiguracionSolapasAnexo
from apps.registro.forms.VerificacionDatosAnexoForm import VerificacionDatosAnexoForm

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
@credential_required('reg_anexo_consulta')
def index(request, anexo_id):
    
    anexo = __get_anexo(request, anexo_id)

    """
    Búsqueda de anexos
    """
    if request.method == 'GET':
        form_filter = AnexoAutoridadFormFilters(request.GET, anexo_id=anexo.id)
    else:
        form_filter = AnexoFormFilters(anexo_id=anexo.id)

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
		
    return my_render(request, 'registro/anexo/autoridades/index.html', {
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'anexo': anexo,
        'alta_habilitada': alta_habilitada,
        'verificado': anexo.get_verificacion_datos().autoridades,
        'datos_verificados': anexo.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasAnexo.get_instance(),
        'actual_page': 'autoridades',
        'form_verificacion': VerificacionDatosAnexoForm(
			dato_verificacion='autoridades', 
			unidad_educativa_id=anexo.id, 
			return_url='anexoAutoridadesIndex', 
			verificado=anexo.get_verificacion_datos().autoridades),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery()


@login_required
@credential_required('reg_anexo_completar')
def create(request, anexo_id):
    
    anexo = __get_anexo(request, anexo_id)
    """
    Alta de autoridad.
    """

    if request.method == 'POST':
        form = AnexoAutoridadForm(request.POST)
        if form.is_valid():
            autoridad = form.save(commit=False)
            autoridad.anexo_id = anexo.id
            autoridad.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('anexoAutoridadEdit', args=[autoridad.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = AnexoAutoridadForm()

    # Chequear si se puede dar de alta
    # XXX: sólo se puede dar de alta un registro por ahora
    alta_habilitada = AnexoAutoridad.objects.filter(anexo__id = anexo.id).count() == 0    
    if not alta_habilitada:  # no debería estar en esta pantalla
        request.set_flash('warning', 'No puede dar de alta más de una autoridad.')
        return HttpResponseRedirect(reverse('anexoAutoridadesIndex', args=[anexo.id]))
    
    return my_render(request, 'registro/anexo/autoridades/new.html', {
        'form': form,
        'anexo': anexo,
    })


@login_required
@credential_required('reg_anexo_completar')
def edit(request, autoridad_id):
    """
    Edición de los datos de una autoridad.
    """    
    autoridad = AnexoAutoridad.objects.get(pk=autoridad_id)
    anexo = __get_anexo(request, autoridad.anexo_id)

    if request.method == 'POST':
        form = AnexoAutoridadForm(request.POST, instance=autoridad)
        if form.is_valid():
            autoridad = form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoAutoridadForm(instance=autoridad)

    return my_render(request, 'registro/anexo/autoridades/edit.html', {
        'form': form,
        'autoridad': autoridad,
        'anexo': anexo,
    })


@login_required
@credential_required('reg_anexo_completar')
def delete(request, autoridad_id):
    autoridad = AnexoAutoridad.objects.get(pk=autoridad_id)
    anexo = __get_anexo(request, autoridad.anexo_id)
    autoridad.delete()
    request.set_flash('success', 'Datos de la autoridad eliminados correctamente.')
    return HttpResponseRedirect(reverse('anexoAutoridadesIndex', args=[anexo.id]))
