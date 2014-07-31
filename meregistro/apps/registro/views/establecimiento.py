# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.models.Turno import Turno
from apps.registro.models.EstablecimientoTurno import EstablecimientoTurno
from apps.registro.models.EstablecimientoInformacionEdilicia import EstablecimientoInformacionEdilicia
from apps.registro.models.EstablecimientoConexionInternet import EstablecimientoConexionInternet
from apps.registro.models.Localidad import Localidad
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.RegistroEstablecimiento import RegistroEstablecimiento
from apps.registro.forms.EstablecimientoFormFilters import EstablecimientoFormFilters
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
from apps.registro.forms.EstablecimientoCambiarEstadoForm import EstablecimientoCambiarEstadoForm
from apps.registro.forms.EstablecimientoDatosBasicosForm import EstablecimientoDatosBasicosForm
from apps.registro.forms.EstablecimientoCreateForm import EstablecimientoCreateForm
from apps.registro.forms.EstablecimientoModificarCueForm import EstablecimientoModificarCueForm
from apps.registro.forms.EstablecimientoContactoForm import EstablecimientoContactoForm
from apps.registro.forms.EstablecimientoAlcancesForm import EstablecimientoAlcancesForm
from apps.registro.forms.EstablecimientoTurnoForm import EstablecimientoTurnoForm
from apps.registro.forms.EstablecimientoFuncionesForm import EstablecimientoFuncionesForm
from apps.registro.forms.EstablecimientoInformacionEdiliciaForm import EstablecimientoInformacionEdiliciaForm
from apps.registro.forms.EstablecimientoConexionInternetForm import EstablecimientoConexionInternetForm
from apps.registro.FSM import FSMEstablecimiento
from apps.registro.models import DependenciaFuncional
from apps.reportes.views.establecimiento import establecimientos as reporte_establecimientos
from apps.reportes.models import Reporte
from apps.backend.models import ConfiguracionSolapasEstablecimiento
from django.contrib import messages

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
        form_filter = EstablecimientoFormFilters(request.GET, jurisdiccion_id=jurisdiccion_id, departamento_id=departamento_id)
    else:
        form_filter = EstablecimientoFormFilters(jurisdiccion_id=jurisdiccion_id, departamento_id=departamento_id)
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
    return my_render(request, 'registro/establecimiento/index.html', {
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
    return filters.buildQuery().order_by('nombre').filter(ambito__path__istartswith=request.get_perfil().ambito.path)


@login_required
@credential_required('reg_establecimiento_nueva')
def create(request):
    """
    Alta de establecimiento.
    """
    if request.method == 'POST':
        form = EstablecimientoCreateForm(request.POST)
        if form.is_valid():
            establecimiento = form.save()
            estado = EstadoEstablecimiento.objects.get(nombre=EstadoEstablecimiento.PENDIENTE)
            establecimiento.registrar_estado(estado)

            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_CREATE, establecimiento)
            request.set_flash('success', 'Datos guardados correctamente.')
            return HttpResponseRedirect(reverse('establecimientoCompletarDatosBasicos', args=[establecimiento.id]))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = EstablecimientoCreateForm()
    if request.get_perfil().jurisdiccion() is not None:
        form.initial = {'codigo_jurisdiccion': request.get_perfil().jurisdiccion().prefijo, 'codigo_tipo_unidad_educativa': Establecimiento.CODIGO_TIPO_UNIDAD_EDUCATIVA, }
        form.fields['dependencia_funcional'].queryset = DependenciaFuncional.objects.filter(jurisdiccion=request.get_perfil().jurisdiccion())
    return my_render(request, 'registro/establecimiento/new.html', {
        'form': form,
        'is_new': True,
    })

@login_required
@credential_required('reg_establecimiento_baja')
def delete(request, establecimiento_id):
    establecimiento = Establecimiento.objects.get(pk=establecimiento_id)
    has_anexos = establecimiento.hasAnexos()
    # TODO: chequear que pertenece al ámbito
    if has_anexos:
        request.set_flash('warning', 'No se puede eliminar el establecimiento porque tiene anexos asociados.')
    elif not establecimiento.isDeletable():
        request.set_flash('warning', 'El establecimiento no se puede eliminar.')
    else:
        establecimiento.delete()
        #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_DELETE, establecimiento)
        request.set_flash('success', 'Registro eliminado correctamente.')
    return HttpResponseRedirect(reverse('establecimiento'))


@login_required
@credential_required('reg_establecimiento_registrar')
def registrar(request, establecimientoId):
    """
    CU 23
    """
    establecimiento = Establecimiento.objects.get(pk=establecimientoId)
    form = __registrar_get_form(request, establecimiento)
    if request.method == 'POST' and __registrar_process(request, form, establecimiento):
            return HttpResponseRedirect(reverse('establecimiento'))
    return __registrar_show_form(request, form, establecimiento)


def __registrar_get_form(request, establecimiento):
    if request.method == 'POST':
        form = EstablecimientoCambiarEstadoForm(request.POST)
    else:
        form = EstablecimientoCambiarEstadoForm()
    form.fields["estado"].choices = map(lambda e: (e.id, e), fsmEstablecimiento.estadosDesde(establecimiento.estadoActual()))
    return form


def __registrar_show_form(request, form, establecimiento):
    return my_render(request, 'registro/establecimiento/registrar.html', {
        'form': form,
        'establecimiento': establecimiento
    })


def __registrar_process(request, form, establecimiento):
    if form.is_valid():
        nuevoEstado = form.cleaned_data['estado']
        try:
            establecimiento.registrar_estado(nuevoEstado, form.cleaned_data['observaciones'])
            request.set_flash('success', 'Establecimiento registrado correctamente.')
            return True
        except:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    return False

@login_required
@credential_required('reg_establecimiento_ver')
def completar_datos(request):
    """
    CU 26

    XXX: Por ahora no usamos esta vista, pero puede que más adelante la necesitemos
    para mostrar info del establecimiento
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'establecimiento': establecimiento,
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance()
    })


@login_required
@credential_required('reg_establecimiento_ver')
def completar_datos_basicos(request, establecimiento_id):
    """
    Edición de los datos básicos de un establecimiento.
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)      
    
    if request.method == 'POST' and request.has_credencial('reg_establecimiento_completar'):
        form = EstablecimientoDatosBasicosForm(request.POST, instance=establecimiento)
        if form.is_valid():
            establecimiento = form.save()
            if __puede_verificar_datos(request):
                v = establecimiento.get_verificacion_datos()
                v.datos_basicos = form.cleaned_data['verificado']
                v.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoDatosBasicosForm(instance=establecimiento)

    parts = establecimiento.get_cue_parts()
    form.initial['codigo_jurisdiccion'] = parts['codigo_jurisdiccion']
    form.initial['cue'] = parts['cue']
    form.initial['codigo_tipo_unidad_educativa'] = parts['codigo_tipo_unidad_educativa']
    form.initial['verificado'] = establecimiento.get_verificacion_datos().datos_basicos
    if request.get_perfil().jurisdiccion() is not None:
        form.fields['dependencia_funcional'].queryset = DependenciaFuncional.objects.filter(jurisdiccion=request.get_perfil().jurisdiccion())
		
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_datos_basicos.html',
        'establecimiento': establecimiento,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })

@login_required
@credential_required('reg_establecimiento_ver')
def completar_contacto(request, establecimiento_id):
    """
    Edición de los datos de contacto de un establecimiento.
    """
    establecimiento = Establecimiento.objects.get(pk=establecimiento_id)

    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')

    if establecimiento.estado.nombre == EstadoEstablecimiento.PENDIENTE:
        if 'reg_editar_establecimiento_pendiente' not in request.get_credenciales():
            raise Exception('Usted no tiene permisos para editar los datos del establecimiento pendiente')

    if request.method == 'POST':
        form = EstablecimientoContactoForm(request.POST, instance=establecimiento)
        if form.is_valid():
            establecimiento = form.save()
            if __puede_verificar_datos(request):
                v = establecimiento.get_verificacion_datos()
                v.contacto = form.cleaned_data['verificado']
                v.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoContactoForm(instance=establecimiento)
    form.initial['verificado'] = establecimiento.get_verificacion_datos().contacto
    
		
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_contacto.html',
        'establecimiento': establecimiento,
        'page_title': 'Contacto',
        'actual_page': 'contacto',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })


@login_required
@credential_required('reg_establecimiento_ver')
def completar_alcances(request, establecimiento_id):
    """
    CU 26
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)

    if request.method == 'POST' and request.has_credencial('reg_establecimiento_completar'):
        form = EstablecimientoAlcancesForm(request.POST, instance=establecimiento)
        if form.is_valid():
            alcances = form.save()
            if __puede_verificar_datos(request):
                v = establecimiento.get_verificacion_datos()
                v.alcances  = form.cleaned_data['verificado']
                v.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoAlcancesForm(instance=establecimiento)

    form.initial['verificado'] = establecimiento.get_verificacion_datos().alcances
		
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_alcances.html',
        'establecimiento': establecimiento,
        'page_title': 'Alcance',
        'actual_page': 'alcances',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })


@login_required
@credential_required('reg_establecimiento_ver')
def completar_funciones(request, establecimiento_id):
    """
    CU 26
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)

    if request.method == 'POST' and request.has_credencial('reg_establecimiento_completar'):
        form = EstablecimientoFuncionesForm(request.POST, instance=establecimiento)
        if form.is_valid():
            funciones = form.save()
            if __puede_verificar_datos(request):
                v = establecimiento.get_verificacion_datos()
                v.funciones = form.cleaned_data['verificado']
                v.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoFuncionesForm(instance=establecimiento)
    form.initial['verificado'] = establecimiento.get_verificacion_datos().funciones
        
		
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_funciones.html',
        'establecimiento': establecimiento,
        'page_title': 'Funciones',
        'actual_page': 'funciones',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })


@login_required
@credential_required('reg_establecimiento_ver')
def completar_informacion_edilicia(request, establecimiento_id):
    """
    CU 26
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)

    try:
        informacion_edilicia = EstablecimientoInformacionEdilicia.objects.get(establecimiento=establecimiento)
    except:
        informacion_edilicia = EstablecimientoInformacionEdilicia()
        informacion_edilicia.establecimiento = establecimiento

    if request.method == 'POST' and request.has_credencial('reg_establecimiento_completar'):
        form = EstablecimientoInformacionEdiliciaForm(request.POST, instance=informacion_edilicia)
        if form.is_valid():
            informacion_edilicia = form.save()
            if __puede_verificar_datos(request):
                v = establecimiento.get_verificacion_datos()
                v.info_edilicia = form.cleaned_data['verificado']
                v.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoInformacionEdiliciaForm(instance=informacion_edilicia)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion=TipoDominio.TIPO_COMPARTIDO).id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion=TipoCompartido.TIPO_OTRA_INSTITUCION).id
    form.initial['verificado'] = establecimiento.get_verificacion_datos().info_edilicia
		
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_informacion_edilicia.html',
        'establecimiento': establecimiento,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
        'page_title': 'Información edilicia',
        'actual_page': 'informacion_edilicia',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })


@login_required
@credential_required('reg_establecimiento_ver')
def completar_conexion_internet(request, establecimiento_id):
    """
    CU 26
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)
    try:
        conexion = EstablecimientoConexionInternet.objects.get(establecimiento=establecimiento)
    except:
        conexion = EstablecimientoConexionInternet()
        conexion.establecimiento = establecimiento

    if request.method == 'POST' and request.has_credencial('reg_establecimiento_completar'):
        form = EstablecimientoConexionInternetForm(request.POST, instance=conexion)
        if form.is_valid():
            conexion = form.save()
            if __puede_verificar_datos(request):
                v = establecimiento.get_verificacion_datos()
                v.conectividad = form.cleaned_data['verificado']
                v.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoConexionInternetForm(instance=conexion)
    form.initial['verificado'] = establecimiento.get_verificacion_datos().conectividad
		
    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_conexion_internet.html',
        'establecimiento': establecimiento,
        'page_title': 'Conectividad',
        'actual_page': 'conexion_internet',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })


@login_required
@credential_required('registro_modificar_cue')
def modificar_cue(request, establecimiento_id):
    """
    CU 26
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)

    if request.method == 'POST':
        form = EstablecimientoModificarCueForm(request.POST, instance=establecimiento)
        if form.is_valid():
            establecimiento = form.save()
           
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = EstablecimientoModificarCueForm(instance=establecimiento)
		

    parts = establecimiento.get_cue_parts()
    form.initial['codigo_jurisdiccion'] = parts['codigo_jurisdiccion']
    form.initial['cue'] = parts['cue']
    form.initial['codigo_tipo_unidad_educativa'] = parts['codigo_tipo_unidad_educativa']

    return my_render(request, 'registro/establecimiento/completar_datos.html', {
        'form': form,
        'form_template': 'registro/establecimiento/form_modificar_cue.html',
        'establecimiento': establecimiento,
        'page_title': 'Modificar CUE',
        'actual_page': 'datos_basicos',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })


@login_required
@credential_required('reg_establecimiento_ver')
def datos_establecimiento(request):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    
    return my_render(request, 'registro/establecimiento/datos_establecimiento.html', {
        'establecimiento': establecimiento,
        'turnos': establecimiento.turnos.all(),
        'funciones': establecimiento.funciones.all(),
        'autoridades': establecimiento.autoridades.all(),
        'alcances': establecimiento.alcances.all(),
        'domicilios': establecimiento.domicilios.all(),
    })


#@credential_required('reg_establecimiento_ver')
def detalle(request, establecimiento_id):
    "Ver de juntar con la función datos_establecimiento"
    try:
        establecimiento = Establecimiento.objects.get(pk=establecimiento_id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except Establecimiento.DoesNotExist:
        raise Exception('El establecimiento no pertenece a su ámbito.')

    return my_render(request, 'registro/establecimiento/datos_establecimiento.html', {
        'establecimiento': establecimiento,
        'turnos': establecimiento.turnos.all(),
        'funciones': establecimiento.funciones.all(),
        'autoridades': establecimiento.autoridades.all(),
        'alcances': establecimiento.alcances.all(),
        'domicilios': establecimiento.domicilios.all(),
    })

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_datos_basicos(request, establecimiento_id):
    """
    Visualización de los datos básicos de un establecimiento.
    """
    establecimiento = __get_establecimiento(request, establecimiento_id)      

    parts = establecimiento.get_cue_parts()
		
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_datos_basicos.html',
        'establecimiento': establecimiento,
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_contacto(request, establecimiento_id):
    """
    Visualización de los datos de contacto de un establecimiento.
    """
    establecimiento = Establecimiento.objects.get(pk=establecimiento_id)

    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
		
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_contacto.html',
        'establecimiento': establecimiento,
        'page_title': 'Contacto',
        'actual_page': 'contacto',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })
    

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_alcances(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')

    verificado = establecimiento.get_verificacion_datos().alcances
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_alcances.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'alcances': establecimiento.alcances.all(),
        'page_title': 'Alcance',
        'actual_page': 'alcances',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })
    

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_turnos(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')

    verificado = establecimiento.get_verificacion_datos().turnos
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_turnos.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'turnos': EstablecimientoTurno.objects.filter(establecimiento=establecimiento).order_by('turno__nombre'),
        'page_title': 'Turnos',
        'actual_page': 'turnos',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })
    

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_funciones(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    verificado = establecimiento.get_verificacion_datos().funciones
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_funciones.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'funciones': establecimiento.funciones.all(),
        'page_title': 'Funciones',
        'actual_page': 'funciones',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })
    

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_domicilios(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    verificado = establecimiento.get_verificacion_datos().domicilios
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_domicilios.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'domicilios': establecimiento.domicilios.all(),
        'page_title': 'Domicilios',
        'actual_page': 'domicilios',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_autoridades(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    verificado = establecimiento.get_verificacion_datos().autoridades
    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_autoridades.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'autoridades': establecimiento.autoridades.all(),
        'page_title': 'Autoridades',
        'actual_page': 'autoridades',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_informacion_edilicia(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    verificado = establecimiento.get_verificacion_datos().info_edilicia

    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_informacion_edilicia.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'informacion_edilicia': establecimiento.establecimientoinformacionedilicia_set.get(),
        'page_title': 'Información Edilicia',
        'actual_page': 'informacion_edilicia',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_conexion_internet(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    verificado = establecimiento.get_verificacion_datos().conectividad

    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_conexion_internet.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'conexion_internet': establecimiento.establecimientoconexioninternet_set.get(),
        'page_title': 'Conexión Internet',
        'actual_page': 'conexion_internet',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })

@login_required
@credential_required('reg_establecimiento_consulta')
def ver_matricula(request, establecimiento_id):
    establecimiento = __get_establecimiento(request, establecimiento_id)
    if not __establecimiento_dentro_del_ambito(request, establecimiento):
        raise Exception('La sede no se encuentra en su ámbito.')
    verificado = establecimiento.get_verificacion_datos().matricula

    return my_render(request, 'registro/establecimiento/ver_datos.html', {
        'template': 'registro/establecimiento/ver_matricula.html',
        'verificado': verificado,
        'establecimiento': establecimiento,
        'matricula': establecimiento.establecimientomatricula_set.all().order_by('anio'),
        'page_title': 'Matrícula',
        'actual_page': 'matricula',
        'configuracion_solapas': ConfiguracionSolapasEstablecimiento.get_instance(),
        'datos_verificados': establecimiento.get_verificacion_datos().get_datos_verificados()
    })
