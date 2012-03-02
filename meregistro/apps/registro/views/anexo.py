# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil
from apps.registro.models.Establecimiento import Establecimiento
from apps.registro.models.Anexo import Anexo
from apps.registro.models.Localidad import Localidad
from apps.registro.models.EstadoAnexo import EstadoAnexo
from apps.registro.models.EstadoEstablecimiento import EstadoEstablecimiento
from apps.registro.models.AnexoEstado import AnexoEstado
from apps.registro.models.AnexoDomicilio import AnexoDomicilio
from apps.registro.models.AnexoInformacionEdilicia import AnexoInformacionEdilicia
from apps.registro.models.AnexoConexionInternet import AnexoConexionInternet
from apps.registro.models.TipoDominio import TipoDominio
from apps.registro.models.TipoCompartido import TipoCompartido
from apps.registro.forms import AnexoFormFilters, AnexoDomicilioForm, AnexoBajaForm, AnexoDatosBasicosForm, AnexoTurnosForm, AnexoDomicilioForm
from apps.registro.forms.AnexoContactoForm import AnexoContactoForm
from apps.registro.forms.AnexoNivelesForm import AnexoNivelesForm
from apps.registro.forms.AnexoFuncionesForm import AnexoFuncionesForm
from apps.registro.forms.AnexoInformacionEdiliciaForm import AnexoInformacionEdiliciaForm
from apps.registro.forms.AnexoConexionInternetForm import AnexoConexionInternetForm
from apps.registro.FSM import FSMAnexo
from apps.registro.forms.AnexoCambiarEstadoForm import AnexoCambiarEstadoForm
from helpers.MailHelper import MailHelper
from django.core.paginator import Paginator
import datetime
from apps.reportes.views.anexo import anexos as reporte_anexos
from apps.reportes.models import Reporte

fsmAnexo = FSMAnexo()

ITEMS_PER_PAGE = 50


def __pertenece_al_establecimiento(request, anexo):
    """
    El anexo pertenece al establecimiento?
    """
    return anexo.establecimiento.ambito.path == request.get_perfil().ambito.path

def __anexo_dentro_del_ambito(request, anexo):
    """
    El anexo está dentro del ámbito?
    """
    try:
        anexo = Anexo.objects.get(id=anexo.id, ambito__path__istartswith=request.get_perfil().ambito.path)
    except anexo.DoesNotExist:
        return False
    return True


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
def index(request):
    """
    Búsqueda de anexos
    """
    if request.method == 'GET':
        form_filter = AnexoFormFilters(request.GET)
    else:
        form_filter = AnexoFormFilters()
    q = build_query(form_filter, 1, request)

    try:
        if request.GET['export'] == '1':
            return reporte_anexos(request, q)
    except KeyError:
        pass

    jurisdiccion = request.get_perfil().jurisdiccion()
    if jurisdiccion is not None:
        form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(dependencia_funcional__jurisdiccion__id=jurisdiccion.id)
    form_filter.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path)
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
    return my_render(request, 'registro/anexo/index.html', {
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
    return filters.buildQuery().order_by('establecimiento__nombre', 'cue').filter(ambito__path__istartswith=request.get_perfil().ambito.path)


@login_required
@credential_required('reg_anexo_alta')
def create(request):
    """
    Alta de anexo.
    """
    if request.method == 'POST':
        form = AnexoDatosBasicosForm(request.POST)
        if form.is_valid():
            anexo = form.save(commit=False)
            estado = EstadoAnexo.objects.get(nombre=EstadoAnexo.PENDIENTE)
            anexo.estado = estado
            anexo.fecha_alta = datetime.date.today()
            anexo.save()
            anexo.registrar_estado()

            MailHelper.notify_by_email(MailHelper.ANEXO_CREATE, anexo)
            request.set_flash('success', 'Datos guardados correctamente.')

            # redirigir al edit
            return HttpResponseRedirect(reverse('anexo'))
        else:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    else:
        form = AnexoDatosBasicosForm()

    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path, estado__nombre=EstadoEstablecimiento.REGISTRADO)
    form.initial = {'codigo_jurisdiccion': '--', 'cue': '-----', }
    return my_render(request, 'registro/anexo/new.html', {
        'form': form,
        'is_new': True,
    })


@login_required
@credential_required('reg_anexo_baja')
def delete(request, anexo_id):
    anexo = Anexo.objects.get(pk=anexo_id)
    if not __anexo_dentro_del_ambito(request, anexo):
        raise Exception('El anexo no está en el ámbito del usuario.')
    elif not anexo.is_deletable():
       request.set_flash('warning', 'El anexo no se puede eliminar.')
    else:
        anexo.delete()
        request.set_flash('success', 'Registro eliminado correctamente.')
    return HttpResponseRedirect(reverse('anexo'))

@login_required
@credential_required('reg_anexo_baja')
def baja(request, anexo_id):
    """
    Baja de un anexo
    CU 28
    """
    anexo = Anexo.objects.get(pk=anexo_id)
    """ Pertenece al establecimiento? """
    pertenece_al_establecimiento = __pertenece_al_establecimiento(request, anexo)
    if not pertenece_al_establecimiento:
        raise Exception('El anexo no pertenece a su establecimiento.')
    """ El anexo ya fue dado de baja? """
    dado_de_baja = anexo.dadoDeBaja()
    if dado_de_baja:
        request.set_flash('notice', 'El anexo ya se encuentra dado de baja.')
    """ Continuar """
    if request.method == 'POST':
        form = AnexoBajaForm(request.POST)
        if form.is_valid():
            baja = form.save(commit=False)
            baja.anexo = anexo
            baja.save()
            estado = EstadoAnexo.objects.get(nombre=EstadoAnexo.BAJA)
            anexo.estado = estado
            anexo.save()
            anexo.registrar_estado()
            dado_de_baja = True

            request.set_flash('success', 'El anexo fue dado de baja correctamente.')
            """ Redirecciono para evitar el reenvío del form """
            return HttpResponseRedirect(reverse('anexo'))
        else:
            request.set_flash('warning', 'Ocurrió un error dando de baja el anexo.')
    else:
        form = AnexoBajaForm()
    return my_render(request, 'registro/anexo/baja.html', {
        'form': form,
        'anexo': anexo,
        'dado_de_baja': dado_de_baja,
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_datos_basicos(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    
    if request.method == 'POST':
        form = AnexoDatosBasicosForm(request.POST, instance=anexo)
        if form.is_valid():
            anexo = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoDatosBasicosForm(instance=anexo)

    parts = anexo.get_cue_parts()
    form.initial['codigo_jurisdiccion'] = parts['codigo_jurisdiccion']
    form.initial['cue'] = parts['cue']
    form.initial['codigo_tipo_unidad_educativa'] = parts['codigo_tipo_unidad_educativa']

    form.fields["establecimiento"].queryset = Establecimiento.objects.filter(ambito__path__istartswith=request.get_perfil().ambito.path, estado__nombre=EstadoEstablecimiento.REGISTRADO)
        
    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_datos_basicos.html',
        'anexo': anexo,
        'codigo_tipo_unidad_educativa': parts['codigo_tipo_unidad_educativa'],
        'page_title': 'Datos básicos',
        'actual_page': 'datos_basicos',
    })

@login_required
@credential_required('reg_anexo_completar')
def completar_contacto(request, anexo_id):
    """
    Edición de los datos de contacto de un anexo.
    """
    anexo = __get_anexo(request, anexo_id)

    if not __anexo_dentro_del_ambito(request, anexo):
        raise Exception('El anexo no se encuentra en su ámbito.')

    if anexo.estado.nombre == EstadoAnexo.PENDIENTE:
        if 'reg_editar_anexo_pendiente' not in request.get_credenciales():
            raise Exception('Usted no tiene permisos para editar los datos del anexo pendiente')

    if request.method == 'POST':
        form = AnexoContactoForm(request.POST, instance=anexo)
        if form.is_valid():
            anexo = form.save()
            MailHelper.notify_by_email(MailHelper.ANEXO_UPDATE, anexo)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoContactoForm(instance=anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_contacto.html',
        'anexo': anexo,
        'page_title': 'Contacto',
        'actual_page': 'contacto',
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_turnos(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    CU 26
    """

    if request.method == 'POST':
        form = AnexoTurnosForm(request.POST, instance=anexo)
        if form.is_valid():
            turnos = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoTurnosForm(instance=anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_turnos.html',
        'anexo': anexo,
        'page_title': 'Turnos',
        'actual_page': 'turnos',
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_domicilio(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    CU 26
    """
    try:
        domicilio = anexo.anexo_domicilio.get()
    except:
        domicilio = AnexoDomicilio()
        domicilio.anexo = anexo

    if request.method == 'POST':
        form = AnexoDomicilioForm(request.POST, instance=domicilio)
        if form.is_valid():
            domicilio = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoDomicilioForm(instance=domicilio)

    jurisdiccion = request.get_perfil().jurisdiccion()
    form.fields["localidad"].queryset = Localidad.objects.filter(departamento__jurisdiccion__id=jurisdiccion.id)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_domicilio.html',
        'anexo': anexo,
        'page_title': 'Domicilio',
        'actual_page': 'domicilio',
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_niveles(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    CU 26
    """

    if request.method == 'POST':
        form = AnexoNivelesForm(request.POST, instance=anexo)
        if form.is_valid():
            niveles = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoNivelesForm(instance=anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_niveles.html',
        'anexo': anexo,
        'page_title': 'Niveles',
        'actual_page': 'niveles',
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_funciones(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    CU 26
    """

    if request.method == 'POST':
        form = AnexoFuncionesForm(request.POST, instance=anexo)
        if form.is_valid():
            funciones = form.save()
            #MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, establecimiento)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoFuncionesForm(instance=anexo)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_funciones.html',
        'anexo': anexo,
        'page_title': 'Funciones',
        'actual_page': 'funciones',
    })


@login_required
#@credential_required('reg_establecimiento_completar')
def completar_informacion_edilicia(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    CU 26
    """

    try:
        informacion_edilicia = AnexoInformacionEdilicia.objects.get(anexo=anexo)
    except:
        informacion_edilicia = AnexoInformacionEdilicia()
        informacion_edilicia.anexo = anexo

    if request.method == 'POST':
        form = AnexoInformacionEdiliciaForm(request.POST, instance=informacion_edilicia)
        if form.is_valid():
            informacion_edilicia = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, anexo)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoInformacionEdiliciaForm(instance=informacion_edilicia)

    es_dominio_compartido_id = TipoDominio.objects.get(descripcion='Compartido').id
    comparte_otro_nivel_id = TipoCompartido.objects.get(descripcion='Establecimiento de otro nivel').id

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_informacion_edilicia.html',
        'anexo': anexo,
        'es_dominio_compartido_id': es_dominio_compartido_id,
        'comparte_otro_nivel_id': comparte_otro_nivel_id,
        'page_title': 'Información edilicia',
        'actual_page': 'informacion_edilicia',
    })


@login_required
#@credential_required('reg_anexo_completar')
def completar_conexion_internet(request, anexo_id):
    anexo = __get_anexo(request, anexo_id)
    """
    CU 26
    """
    try:
        conexion = AnexoConexionInternet.objects.get(anexo=anexo)
    except:
        conexion = AnexoConexionInternet()
        conexion.anexo = anexo

        form = AnexoConexionInternetForm(request.POST, instance=conexion)
        if form.is_valid():
            conexion = form.save()
            MailHelper.notify_by_email(MailHelper.ESTABLECIMIENTO_UPDATE, anexo)
            request.set_flash('success', 'Datos actualizados correctamente.')
        else:
            request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
    else:
        form = AnexoConexionInternetForm(instance=conexion)

    return my_render(request, 'registro/anexo/completar_datos.html', {
        'form': form,
        'form_template': 'registro/anexo/form_conexion_internet.html',
        'anexo': anexo,
        'page_title': 'Conexión a internet',
        'actual_page': 'conexion_internet',
    })


@login_required
@credential_required('reg_anexo_aprobar_registro')
def registrar(request, anexo_id):
    anexo = Anexo.objects.get(pk=anexo_id)
    form = __registrar_get_form(request, anexo)
    if request.method == 'POST' and __registrar_process(request, form, anexo):
            return HttpResponseRedirect(reverse('anexo'))
    return __registrar_show_form(request, form, anexo)


def __registrar_get_form(request, anexo):
    if request.method == 'POST':
        form = AnexoCambiarEstadoForm(request.POST)
    else:
        form = AnexoCambiarEstadoForm()
    form.fields["estado"].choices = map(lambda e: (e.id, e), fsmAnexo.estadosDesde(anexo.estado_actual))
    return form


def __registrar_show_form(request, form, anexo):
    return my_render(request, 'registro/anexo/registrar.html', {
        'form': form,
        'anexo': anexo
    })


def __registrar_process(request, form, anexo):
    if form.is_valid():
        nuevoEstado = form.cleaned_data['estado']
        try:
            anexo.estado = nuevoEstado
            anexo.save()
            anexo.registrar_estado()
            request.set_flash('success', 'Anexo registrado correctamente.')
            return True
        except:
            request.set_flash('warning', 'Ocurrió un error guardando los datos.')
    return False
