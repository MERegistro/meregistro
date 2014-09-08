# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Ambito, Rol
from apps.registro.models import Establecimiento, EstadoEstablecimiento, Anexo, EstadoAnexo
from apps.titulos.models import TituloNacional, EstadoTituloNacional, EstadoNormativaJurisdiccional, NormativaJurisdiccional
from apps.validez_nacional.forms import SolicitudFormFilters, SolicitudDatosBasicosForm, SolicitudNormativasForm,\
    SolicitudCohortesForm, SolicitudControlForm, ValidezInstitucionalFormFilters, SolicitudAsignacionFormFilters
from apps.validez_nacional.models import EstadoSolicitud, Solicitud, SolicitudEstablecimiento, ValidezNacional
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.reportes.views.validez_nacional import solicitudes as reporte_solicitudes
from apps.reportes.views.solicitud import detalle_numeracion as reporte_detalle_numeracion
from apps.reportes.models import Reporte
from apps.validez_nacional.FSM import FSMSolicitud

ITEMS_PER_PAGE = 50
fsmSolicitud = FSMSolicitud()

def __puede_editarse_solicitud(request, solicitud):
    # Sólo se puede editar mientras está en estado Pendiente
    # pero el AdminNacional puede hacerlo mientras no esté numerado
    return (solicitud.estado.nombre == EstadoSolicitud.PENDIENTE) or \
        (solicitud.estado.nombre != EstadoSolicitud.NUMERADO and request.get_perfil().rol.nombre == Rol.ROL_ADMIN_NACIONAL)
    

def __flat_list(list_to_flat):
    "Método para aplanar las listas"
    return [i for j in list_to_flat for i in j]
    

@login_required
@credential_required('validez_nacional_solicitud_consulta')
def index(request):
    
    if request.method == 'GET':
        form_filter = SolicitudFormFilters(request.GET)
    else:
        form_filter = SolicitudFormFilters()
    q = build_query(form_filter, 1, request)

    try:
        if request.GET['export'] == '1':
            return reporte_solicitudes(request, q)
    except KeyError:
        pass
        
    if request.get_perfil().jurisdiccion():
        q = q.filter(jurisdiccion__id=request.get_perfil().jurisdiccion().id)
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

    return my_render(request, 'validez_nacional/solicitud/index.html', {
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
    return filters.buildQuery().order_by('-estado__nombre', 'jurisdiccion__nombre', 'primera_cohorte')


@login_required
@credential_required('validez_nacional_solicitud_create')
def create(request):
    try:
        jurisdiccion_id = jurisdiccion_id=request.get_perfil().jurisdiccion().id
    except AttributeError:
        jurisdiccion_id = None
    if request.method == 'POST':
        form = SolicitudDatosBasicosForm(request.POST, jurisdiccion_id=jurisdiccion_id)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.estado = EstadoSolicitud.objects.get(nombre=EstadoSolicitud.PENDIENTE)
            solicitud.jurisdiccion = request.get_perfil().jurisdiccion()
            solicitud.save()
            
            solicitud.registrar_estado()

            request.set_flash('success', 'Datos guardados correctamente.')

            return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = SolicitudDatosBasicosForm(jurisdiccion_id=jurisdiccion_id)
    # Agrego el filtro por jurisdicción
    return my_render(request, 'validez_nacional/solicitud/new.html', {
        'form': form,
        'form_template': 'validez_nacional/solicitud/form_datos_basicos.html',
        'is_new': True,
        'page_title': 'Título',
        'current_page': 'datos_basicos',
    })


@login_required
@credential_required('validez_nacional_solicitud_editar')
# Editar datos básicos
def edit(request, solicitud_id):
    """
    Edición de los datos de un título jurisdiccional.
    """
    solicitud = Solicitud.objects.get(pk=solicitud_id)
    
    if not __puede_editarse_solicitud(request, solicitud):
        request.set_flash('warning', 'No puede editarse la solicitud.')
        return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
    
    estado_id = solicitud.estado_id
        
    if request.method == 'POST':
        form = SolicitudDatosBasicosForm(request.POST, instance=solicitud, jurisdiccion_id=solicitud.jurisdiccion_id)
        if form.is_valid():
            sol = form.save(commit=False)
            sol.id = solicitud.id
            sol.jurisdiccion_id = solicitud.jurisdiccion_id
            sol.estado_id = solicitud.estado_id
            form.save()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = SolicitudDatosBasicosForm(instance=solicitud, jurisdiccion_id=solicitud.jurisdiccion_id)
    return my_render(request, 'validez_nacional/solicitud/edit.html', {
        'form': form,
        'solicitud': solicitud,
        'form_template': 'validez_nacional/solicitud/form_datos_basicos.html',
        'is_new': False,
        'page_title': 'Título',
        'current_page': 'datos_basicos',
    })


@login_required
@credential_required('validez_nacional_solicitud_editar')
def editar_normativas(request, solicitud_id):
    """
    Edición de normativas
    """
    try:
        solicitud = Solicitud.objects.get(pk=solicitud_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'validez_nacional/solicitud/new.html', {
            'solicitud': None,
            'form_template': 'validez_nacional/solicitud/form_normativas.html',
            'page_title': 'Normativas',
            'current_page': 'normativas',
    })

    if not __puede_editarse_solicitud(request, solicitud):
        request.set_flash('warning', 'No puede editarse la solicitud.')
        return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
        
    if request.method == 'POST':
        form = SolicitudNormativasForm(request.POST, instance=solicitud)
        if form.is_valid():
            normativas = form.save()

            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('solicitudNormativasEdit', args=[solicitud.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = SolicitudNormativasForm(instance=solicitud)
        
    current_ids = [n.id for n in solicitud.normativas_jurisdiccionales.all().order_by('numero_anio')]
    restantes_ids = [n.id for n in NormativaJurisdiccional.objects.filter(jurisdiccion=solicitud.jurisdiccion).exclude(id__in=current_ids).order_by('numero_anio')]

    # http://blog.mathieu-leplatre.info/django-create-a-queryset-from-a-list-preserving-order.html
    pk_list = current_ids + restantes_ids
    clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(pk_list)])
    ordering = 'CASE %s END' % clauses
    queryset = NormativaJurisdiccional.objects.filter(pk__in=pk_list).extra(
               select={'ordering': ordering}, order_by=('ordering',))

    form.fields['normativas_jurisdiccionales'].queryset = queryset


    return my_render(request, 'validez_nacional/solicitud/edit.html', {
        'form': form,
        'solicitud': solicitud,
        'form_template': 'validez_nacional/solicitud/form_normativas.html',
        'is_new': False,
        'page_title': 'Normativas',
        'current_page': 'normativas',
    })


@login_required
@credential_required('validez_nacional_solicitud_editar')
def editar_cohortes(request, solicitud_id):
    """
    Edición de datos de cohortes
    """
    try:
        solicitud = Solicitud.objects.get(pk=solicitud_id)
    except:
        # Es nuevo, no mostrar el formulario antes de que guarden los datos básicos
        return my_render(request, 'validez_nacional/solicitud/new.html', {
        'solicitud': None,
        'is_new': True,
        'form_template': 'validez_nacional/solicitud/form_cohortes.html',
        'page_title': 'Cohortes',
        'current_page': 'cohortes',
    })

    if not __puede_editarse_solicitud(request, solicitud):
        request.set_flash('warning', 'No puede editarse la solicitud.')
        return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
        
    if request.method == 'POST':
        form = SolicitudCohortesForm(request.POST, instance=solicitud)
        if form.is_valid():
            cohorte = form.save()
            request.set_flash('success', 'Datos guardados correctamente.')
            # redirigir a edit
            return HttpResponseRedirect(reverse('solicitudCohortesEdit', args=[solicitud.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = SolicitudCohortesForm(instance=solicitud)
    return my_render(request, 'validez_nacional/solicitud/edit.html', {
        'form': form,
        'solicitud': solicitud,
        'form_template': 'validez_nacional/solicitud/form_cohortes.html',
        'is_new': solicitud.primera_cohorte is None and solicitud.ultima_cohorte is None,
        'page_title': 'Cohortes',
        'current_page': 'cohortes',
    })


@login_required
@credential_required('validez_nacional_solicitud_control')
def control(request, solicitud_id):
    solicitud = Solicitud.objects.get(pk=solicitud_id)
    estado_anterior = solicitud.estado

    #raise Exception(estado_anterior)
    if request.method == 'POST':
        form = SolicitudControlForm(request.POST, instance=solicitud)
        if form.is_valid():
            sol = form.save()
            if sol.estado != estado_anterior:
                sol.registrar_estado()

            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = SolicitudControlForm(instance=solicitud)

    form.fields["estado"].choices = map(lambda e: (e.id, e), fsmSolicitud.estadosDesde(solicitud.estado))

    return my_render(request, 'validez_nacional/solicitud/edit.html', {
        'form': form,
        'solicitud': solicitud,
        'form_template': 'validez_nacional/solicitud/form_control.html',
        'is_new': False,
        'page_title': 'Control de Solicitud',
        'current_page': 'control',
    })


@login_required
@credential_required('validez_nacional_solicitud_editar')
def asignar_establecimientos(request, solicitud_id):
    solicitud = Solicitud.objects.get(pk=solicitud_id)

    if not __puede_editarse_solicitud(request, solicitud):
        request.set_flash('warning', 'No puede editarse la solicitud.')
        return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))

    form_filter = SolicitudAsignacionFormFilters(request.GET, tipo_ue='Establecimiento', solicitud=solicitud)
    q = form_filter.buildQuery()
    
    "Traigo los ids de los establecimientos actualmente asignados a la solicitud"
    current_establecimientos_ids = __flat_list(solicitud.establecimientos.all().values_list("establecimiento_id"))
    
    q1 = q.filter(solicitudes__establecimiento__id__in=current_establecimientos_ids).order_by('cue') # seleccionados
    q2 = q.exclude(id__in=[e.id for e in q1]).order_by('cue') # no seleccionados
    
    from itertools import chain
    res = list(chain(q1, q2))
    
    
    paginator = Paginator(res, ITEMS_PER_PAGE)

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
    
    "Procesamiento"
    if request.method == 'POST':
        values_dict = {
            'establecimientos_procesados_ids': [e.id for e in objects], #  Son los establecimientos de la página actual
            'current_establecimientos_ids': current_establecimientos_ids,
            'establecimientos_seleccionados_ids': request.POST.getlist("establecimientos"),
        }
        
        solicitud.save_establecimientos(**values_dict)

        request.set_flash('success', 'Datos actualizados correctamente.')
        # redirigir a edit
        return HttpResponseRedirect(reverse('solicitudAsignarEstablecimientos', args=[solicitud.id]))

    return my_render(request, 'validez_nacional/solicitud/asignar_establecimientos.html', {
        'solicitud': solicitud,
        'form_filters': form_filter,
        'current_establecimientos_ids': current_establecimientos_ids,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })
    
    
@login_required
@credential_required('validez_nacional_solicitud_editar')
def asignar_anexos(request, solicitud_id):
    solicitud = Solicitud.objects.get(pk=solicitud_id)

    if not __puede_editarse_solicitud(request, solicitud):
        request.set_flash('warning', 'No puede editarse la solicitud.')
        return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
        
    form_filter = SolicitudAsignacionFormFilters(request.GET, tipo_ue='Anexo', solicitud=solicitud)
    q = form_filter.buildQuery()
    
    "Traigo los ids de los establecimientos actualmente asignados a la solicitud"
    current_anexos_ids = __flat_list(solicitud.anexos.all().values_list("anexo_id"))
    
    
    q1 = q.filter(solicitudes__anexo__id__in=current_anexos_ids).order_by('cue') # seleccionados
    q2 = q.exclude(id__in=[a.id for a in q1]).order_by('cue') # no seleccionados
    
    from itertools import chain
    res = list(chain(q1, q2))
    
    paginator = Paginator(res, ITEMS_PER_PAGE)

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
    
    "Procesamiento"
    if request.method == 'POST':
        values_dict = {
            'anexos_procesados_ids': [a.id for a in objects], #  Son los establecimientos de la página actual
            'current_anexos_ids': current_anexos_ids,
            'anexos_seleccionados_ids': request.POST.getlist("anexos"),
        }
        
        solicitud.save_anexos(**values_dict)

        request.set_flash('success', 'Datos actualizados correctamente.')
        # redirigir a edit
        return HttpResponseRedirect(reverse('solicitudAsignarAnexos', args=[solicitud.id]))

    return my_render(request, 'validez_nacional/solicitud/asignar_anexos.html', {
        'solicitud': solicitud,
        'form_filters': form_filter,
        'current_anexos_ids': current_anexos_ids,
        'objects': objects,
        'paginator': paginator,
        'page': page,
        'page_number': page_number,
        'pages_range': range(1, paginator.num_pages + 1),
        'next_page': page_number + 1,
        'prev_page': page_number - 1
    })


@login_required
@credential_required('validez_nacional_solicitud_eliminar')
def delete(request, solicitud_id):
    solicitud = Solicitud.objects.get(pk=solicitud_id)

    if solicitud.is_deletable():
        solicitud.delete()
        request.set_flash('success', 'Registro eliminado correctamente.')
    else:
        request.set_flash('warning', 'El registro no puede ser eliminado.')
    return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))
    


def build_query_institucional(filters, page, request):
    """
    Construye el query de búsqueda a partir de los filtros.
    """
    return filters.buildQuery().order_by('cue')
    
    
@login_required
@credential_required('validez_nacional_solicitud_consulta_institucional')
def consulta_institucional(request):

    ambito = request.get_perfil().ambito
    perfil_establecimiento = ambito.tipo.nombre == Ambito.TIPO_ESTABLECIMIENTO
    perfil_anexo = ambito.tipo.nombre == Ambito.TIPO_ANEXO

    if perfil_establecimiento:
        establecimiento = Establecimiento.objects.get(ambito__path=ambito.path)
        anexos = establecimiento.anexos.all()
    elif perfil_anexo:
        establecimiento = Establecimiento.objects.get(anexos__ambito__path__istartswith=ambito.path)
        anexos = establecimiento.anexos.all()
        
    if request.method == 'GET':
        form_filter = ValidezInstitucionalFormFilters(request.GET, establecimiento=establecimiento)
    else:
        form_filter = ValidezInstitucionalFormFilters(establecimiento=establecimiento)
    q = build_query_institucional(form_filter, 1, request)

    """
    try:
        if request.GET['export'] == '1':
            return reporte_solicitudes(request, q)
    except KeyError:
        pass
    """
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
    return my_render(request, 'validez_nacional/solicitud/consulta_institucional.html', {
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



@login_required
@credential_required('validez_nacional_solicitud_numerar')
def numerar(request, solicitud_id):
    solicitud = Solicitud.objects.get(pk=solicitud_id)
    
    if len(solicitud.normativas_jurisdiccionales.all()) > 0:
        normativas_jurisdiccionales = ', '.join([n.numero_anio for n in solicitud.normativas_jurisdiccionales.all().order_by('numero_anio')])
    else: 
        normativas_jurisdiccionales = solicitud.normativa_jurisdiccional_migrada
        
    if not solicitud.is_numerable():
        request.set_flash('warning', 'La solicitud no se puede numerar.')
        return HttpResponseRedirect(reverse('validezNacionalSolicitudIndex'))

    solicitud_establecimientos = solicitud.establecimientos.all()
    solicitud_anexos = solicitud.anexos.all()

    if request.method == 'POST':
        
        import time
        referencia = str(int(time.time()))
        
        solicitud.estado = EstadoSolicitud.objects.get(nombre=EstadoSolicitud.NUMERADO)
        solicitud.save()
        solicitud.registrar_estado()
        
        # solicitud-establecimientos
        for se in solicitud_establecimientos:
            v = ValidezNacional()
            v.tipo_unidad_educativa = 'Sede'
            v.unidad_educativa_id = se.establecimiento.id
            v.cue = se.establecimiento.cue
            v.solicitud_id = solicitud.id
            v.carrera = solicitud.carrera.nombre
            v.titulo_nacional = solicitud.titulo_nacional.nombre
            v.primera_cohorte = solicitud.primera_cohorte
            v.ultima_cohorte = solicitud.ultima_cohorte
            v.dictamen_cofev = solicitud.dictamen_cofev
            v.normativas_nacionales = solicitud.normativas_nacionales
            v.normativa_jurisdiccional = normativas_jurisdiccionales
            v.referencia = referencia
            v.save() # Necesito recuperar el ID en la siguiente línea
            v.nro_infd = v.calcular_nro_infd_establecimiento()
            v.save()
                
        # solicitud-anexos
        for sa in solicitud_anexos:
            v = ValidezNacional()
            v.tipo_unidad_educativa = 'Anexo'
            v.unidad_educativa_id = sa.anexo.id
            v.cue = sa.anexo.cue
            v.solicitud_id = solicitud.id
            v.carrera = solicitud.carrera.nombre
            v.titulo_nacional = solicitud.titulo_nacional.nombre
            v.primera_cohorte = solicitud.primera_cohorte
            v.ultima_cohorte = solicitud.ultima_cohorte
            v.dictamen_cofev = solicitud.dictamen_cofev
            v.normativas_nacionales = solicitud.normativas_nacionales
            v.normativa_jurisdiccional = normativas_jurisdiccionales
            v.referencia = referencia
            v.save() # Necesito recuperar el ID en la siguiente línea
            v.nro_infd = v.calcular_nro_infd_anexo()
            v.save()
            
        request.set_flash('success', 'Se ha generado la validez de títulos.')
        return HttpResponseRedirect(reverse('validezNacionalDetalleNumeracion', args=[solicitud.id, referencia]))
            
    return my_render(request, 'validez_nacional/solicitud/numerar.html', {
        'solicitud': solicitud,
        'solicitud_establecimientos': solicitud_establecimientos,
        'solicitud_anexos': solicitud_anexos,
        'normativas_jurisdiccionales': normativas_jurisdiccionales,
    })


@login_required
@credential_required('validez_nacional_solicitud_numerar')
def detalle_numeracion(request, solicitud_id, referencia):
    solicitud = Solicitud.objects.get(pk=solicitud_id)
    validez = ValidezNacional.objects.filter(solicitud=solicitud, referencia=referencia)    

    if 'export' in request.GET:
        return reporte_detalle_numeracion(request, validez)
            
    return my_render(request, 'validez_nacional/solicitud/detalle_numeracion.html', {
        'solicitud': solicitud,
        'validez': validez,
        'export_url': Reporte.build_export_url(request.build_absolute_uri()),
    })

@login_required
@credential_required('validez_nacional_solicitud_informe')
def informe(request, solicitud_id):
    solicitud = Solicitud.objects.get(pk=solicitud_id, estado__nombre=EstadoSolicitud.PENDIENTE)
            
    return my_render(request, 'validez_nacional/solicitud/informe.html', {
        'solicitud': solicitud,
    })
