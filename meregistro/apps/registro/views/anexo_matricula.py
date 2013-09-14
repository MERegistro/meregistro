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
from apps.registro.models.AnexoMatricula import AnexoMatricula
from apps.registro.forms.AnexoMatriculaForm import AnexoMatriculaForm
from apps.registro.forms.AnexoMatriculaFormFilters import AnexoMatriculaFormFilters
from apps.backend.models import ConfiguracionSolapasAnexo
from apps.registro.forms.VerificacionDatosAnexoForm import VerificacionDatosAnexoForm

ITEMS_PER_PAGE = 50

@login_required
def __pertenece_al_anexo(request, anexo):
    """
    El anexo pertenece al anexo?
    """
    return anexo.anexo.ambito.path == request.get_perfil().ambito.path

@login_required
def __anexo_dentro_del_ambito(request, anexo):
    """
    El anexo está dentro del ámbito?
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
        raise Exception('El anexo no se encuentra en su ámbito.')

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
        form_filter = AnexoMatriculaFormFilters(request.GET, anexo_id=anexo.id)
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
		
    return my_render(request, 'registro/anexo/matricula/index.html', {
        'anexo': anexo,
        'form_filters': form_filter,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1,
        'verificado': anexo.get_verificacion_datos().matricula,
        'datos_verificados': anexo.get_verificacion_datos().get_datos_verificados(),
        'configuracion_solapas': ConfiguracionSolapasAnexo.get_instance(),
        'actual_page': 'matricula',
        'form_verificacion': VerificacionDatosAnexoForm(
			dato_verificacion='matricula', 
			unidad_educativa_id=anexo.id, 
			return_url='anexoMatriculaIndex', 
			verificado=anexo.get_verificacion_datos().matricula),
    })


def build_query(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('anio')


@login_required
@credential_required('reg_anexo_completar')
def create(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    Alta de matricula.
    """

    if request.method == 'POST':
        form = AnexoMatriculaForm(request.POST, anexo=anexo)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.anexo_id = anexo.id
            matricula.set_formacion_continua()
            matricula.set_formacion_docente()
            matricula.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('anexoMatriculaIndex', args=[matricula.anexo_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = AnexoMatriculaForm(anexo=anexo)
    return my_render(request, 'registro/anexo/matricula/new.html', {
        'anexo': anexo,
        'form': form,
    })


@login_required
@credential_required('reg_anexo_completar')
def edit(request, matricula_id):
    """
    Edición de los datos de una matricula.
    """
    matricula = AnexoMatricula.objects.get(pk=matricula_id)
    anexo = __get_anexo(request, matricula.anexo_id)

    if request.method == 'POST':
        form = AnexoMatriculaForm(request.POST, instance=matricula, anexo=anexo)
        if form.is_valid():
            matricula = form.save(commit=False)
            matricula.set_formacion_continua()
            matricula.set_formacion_docente()
            matricula.save()
            request.set_flash('success', 'Datos actualizados correctamente.')
            return HttpResponseRedirect(reverse('anexoMatriculaIndex', args=[matricula.anexo_id]))
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoMatriculaForm(instance=matricula, anexo=anexo)

    return my_render(request, 'registro/anexo/matricula/edit.html', {
        'form': form,
        'matricula': matricula,
        'anexo': anexo,
    })


@login_required
@credential_required('reg_anexo_completar')
def delete(request, matricula_id):
    matricula = AnexoMatricula.objects.get(pk=matricula_id)
    anexo = __get_anexo(request, matricula.anexo_id)
    
    matricula.delete()
    request.set_flash('success', 'Datos del matricula eliminados correctamente.')
    return HttpResponseRedirect(reverse('anexoMatriculaIndex', args=[matricula.anexo_id]))
