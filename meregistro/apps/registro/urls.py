# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.registro.views.index', name='home'),
    url(r'^establecimiento$', 'apps.registro.views.establecimiento.index', name='establecimiento'),
    url(r'^establecimiento/create', 'apps.registro.views.establecimiento.create', name='establecimientoCreate'),
    url(r'^establecimiento/([0-9]+)/delete', 'apps.registro.views.establecimiento.delete', name='establecimientoDelete'),
    # completar datos del establecimiento
    url(r'^establecimiento/completar_datos/', 'apps.registro.views.establecimiento.completar_datos', name='establecimientoCompletarDatos'),
    url(r'^establecimiento/([0-9]+)/completar_datos_basicos/', 'apps.registro.views.establecimiento.completar_datos_basicos', name='establecimientoCompletarDatosBasicos'),
    url(r'^establecimiento/([0-9]+)/completar_contacto/', 'apps.registro.views.establecimiento.completar_contacto', name='establecimientoCompletarContacto'),
    url(r'^establecimiento/([0-9]+)/completar_niveles/', 'apps.registro.views.establecimiento.completar_niveles', name='establecimientoCompletarNiveles'),
    url(r'^establecimiento/([0-9]+)/completar_turnos/', 'apps.registro.views.establecimiento.completar_turnos', name='establecimientoCompletarTurnos'),
    url(r'^establecimiento/([0-9]+)/completar_funciones/', 'apps.registro.views.establecimiento.completar_funciones', name='establecimientoCompletarFunciones'),
    url(r'^establecimiento/([0-9]+)/completar_informacion_edilicia/', 'apps.registro.views.establecimiento.completar_informacion_edilicia', name='establecimientoCompletarInformacionEdilicia'),
    url(r'^establecimiento/([0-9]+)/completar_conexion_internet/', 'apps.registro.views.establecimiento.completar_conexion_internet', name='establecimientoCompletarConexionInternet'),
    url(r'^establecimiento/([0-9]+)/registrar', 'apps.registro.views.establecimiento.registrar', name='establecimientoRegistrar'),
    url(r'^establecimiento/datos$', 'apps.registro.views.establecimiento.datos_establecimiento', name='establecimientoDatos'),
    url(r'^establecimiento/([0-9]+)/detalle$', 'apps.registro.views.establecimiento.detalle', name='establecimientoDetalle'),
    url(r'^establecimiento/([0-9]+)/revisar_jurisdiccion', 'apps.registro.views.establecimiento.revisar_jurisdiccion', name='establecimientoRevisarJurisdiccion'),
    # establecimiento domicilios
    url(r'^establecimiento/([0-9]+)/domicilios$', 'apps.registro.views.establecimiento_domicilio.index', name='establecimientoDomiciliosIndex'),
    url(r'^establecimiento/([0-9]+)/agregar_domicilio$', 'apps.registro.views.establecimiento_domicilio.create', name='establecimientoDomicilioCreate'),
    url(r'^establecimiento/domicilios/([0-9]+)/edit$', 'apps.registro.views.establecimiento_domicilio.edit', name='establecimientoDomicilioEdit'),
    url(r'^establecimiento/domicilios/([0-9]+)/delete$', 'apps.registro.views.establecimiento_domicilio.delete', name='establecimientoDomicilioDelete'),
    # establecimiento autoridades
    url(r'^establecimiento/autoridades$', 'apps.registro.views.establecimiento_autoridad.index', name='establecimientoAutoridadesIndex'),
    url(r'^establecimiento/agregar_autoridad$', 'apps.registro.views.establecimiento_autoridad.create', name='establecimientoAutoridadCreate'),
    url(r'^establecimiento/autoridades/([0-9]+)/edit$', 'apps.registro.views.establecimiento_autoridad.edit', name='establecimientoAutoridadEdit'),
    url(r'^establecimiento/autoridades/([0-9]+)/delete$', 'apps.registro.views.establecimiento_autoridad.delete', name='establecimientoAutoridadDelete'),
    # anexo
    url(r'^anexo$', 'apps.registro.views.anexo.index', name='anexo'),
    url(r'^anexo/create', 'apps.registro.views.anexo.create', name='anexoCreate'),
    url(r'^anexo/([0-9]+)/baja', 'apps.registro.views.anexo.baja', name='anexoBaja'),
    url(r'^anexo/([0-9]+)/delete', 'apps.registro.views.anexo.delete', name='anexoDelete'),
    url(r'^anexo/([0-9]+)/completar_datos_basicos/', 'apps.registro.views.anexo.completar_datos_basicos', name='anexoCompletarDatosBasicos'),
    url(r'^anexo/([0-9]+)/completar_contacto/', 'apps.registro.views.anexo.completar_contacto', name='anexoCompletarContacto'),
    url(r'^anexo/([0-9]+)/completar_turnos/', 'apps.registro.views.anexo.completar_turnos', name='anexoCompletarTurnos'),
    url(r'^anexo/([0-9]+)/completar_niveles/', 'apps.registro.views.anexo.completar_niveles', name='anexoCompletarNiveles'),
    url(r'^anexo/([0-9]+)/completar_funciones/', 'apps.registro.views.anexo.completar_funciones', name='anexoCompletarFunciones'),
    url(r'^anexo/([0-9]+)/completar_informacion_edilicia/', 'apps.registro.views.anexo.completar_informacion_edilicia', name='anexoCompletarInformacionEdilicia'),
    url(r'^anexo/([0-9]+)/completar_conexion_internet/', 'apps.registro.views.anexo.completar_conexion_internet', name='anexoCompletarConexionInternet'),
    url(r'^anexo/([0-9]+)/registrar', 'apps.registro.views.anexo.registrar', name='anexoRegistrar'),
    # anexo domicilios
    url(r'^anexo/([0-9]+)/domicilios$', 'apps.registro.views.anexo_domicilio.index', name='anexoDomiciliosIndex'),
    url(r'^anexo/([0-9]+)/agregar_domicilio$', 'apps.registro.views.anexo_domicilio.create', name='anexoDomicilioCreate'),
    url(r'^anexo/domicilios/([0-9]+)/edit$', 'apps.registro.views.anexo_domicilio.edit', name='anexoDomicilioEdit'),
    url(r'^anexo/domicilios/([0-9]+)/delete$', 'apps.registro.views.anexo_domicilio.delete', name='anexoDomicilioDelete'),
    # extensiones aulicas
    url(r'^extension_aulica$', 'apps.registro.views.extension_aulica.index', name='extensionAulica'),
    url(r'^extension_aulica/([0-9]+)/edit', 'apps.registro.views.extension_aulica.edit', name='extensionAulicaEdit'),
    url(r'^extension_aulica/create', 'apps.registro.views.extension_aulica.create', name='extensionAulicaCreate'),
    url(r'^extension_aulica/([0-9]+)/baja', 'apps.registro.views.extension_aulica.baja', name='extensionAulicaBaja'),
    url(r'^extension_aulica/([0-9]+)/delete', 'apps.registro.views.extension_aulica.delete', name='extensionAulicaDelete'),
    # dependencias funcionales
    url(r'^dependencia_funcional$', 'apps.registro.views.dependencia_funcional.index', name='dependenciaFuncional'),
    url(r'^dependencia_funcional/([0-9]+)/edit', 'apps.registro.views.dependencia_funcional.edit', name='dependenciaFuncionalEdit'),
    url(r'^dependencia_funcional/create', 'apps.registro.views.dependencia_funcional.create', name='dependenciaFuncionalCreate'),
    url(r'^dependencia_funcional/([0-9]+)/delete', 'apps.registro.views.dependencia_funcional.delete', name='dependenciaFuncionalDelete'),
    # AJAX
    url(r'^ajax/get_localidades_por_departamento/(?P<departamento_id>[0-9]+)', 'apps.registro.views.ajax.get_localidades_por_departamento', name='ajaxGetLocalidadesPorTipo'),
    url(r'^ajax/get_departamentos_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.registro.views.ajax.get_departamentos_por_jurisdiccion', name='ajaxGetDepartamentosPorJurisdiccion'),
    url(r'^ajax/get_cue_parts_from_sede/(?P<sede_id>[0-9]+)', 'apps.registro.views.ajax.get_cue_parts_from_sede', name='ajaxGetCuePartsFromSede'),
   )
