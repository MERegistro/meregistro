# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.registro.views.index', name = 'home'),
    url(r'^establecimiento$', 'apps.registro.views.establecimiento.index', name = 'establecimiento'),
    url(r'^establecimiento/([0-9]+)/edit', 'apps.registro.views.establecimiento.edit', name = 'establecimientoEdit'),
    url(r'^establecimiento/create', 'apps.registro.views.establecimiento.create', name = 'establecimientoCreate'),
    url(r'^establecimiento/([0-9]+)/delete', 'apps.registro.views.establecimiento.delete', name = 'establecimientoDelete'),
    url(r'^establecimiento/completar_datos/', 'apps.registro.views.establecimiento.completar_datos', name = 'establecimientoCompletarDatos'),
    url(r'^establecimiento/completar_datos_basicos/', 'apps.registro.views.establecimiento.completar_datos_basicos', name = 'establecimientoCompletarDatosBasicos'),
    url(r'^establecimiento/completar_niveles/', 'apps.registro.views.establecimiento.completar_niveles', name = 'establecimientoCompletarNiveles'),
    url(r'^establecimiento/completar_turnos/', 'apps.registro.views.establecimiento.completar_turnos', name = 'establecimientoCompletarTurnos'),
    url(r'^establecimiento/completar_funciones/', 'apps.registro.views.establecimiento.completar_funciones', name = 'establecimientoCompletarFunciones'),
    url(r'^establecimiento/completar_domicilio/', 'apps.registro.views.establecimiento.completar_domicilio', name = 'establecimientoCompletarDomicilio'),
    url(r'^establecimiento/completar_informacion_edilicia/', 'apps.registro.views.establecimiento.completar_informacion_edilicia', name = 'establecimientoCompletarInformacionEdilicia'),
    url(r'^establecimiento/completar_conexion_internet/', 'apps.registro.views.establecimiento.completar_conexion_internet', name = 'establecimientoCompletarConexionInternet'),
    url(r'^establecimiento/([0-9]+)/registrar', 'apps.registro.views.establecimiento.registrar', name = 'establecimientoRegistrar'),
    url(r'^establecimiento/datos$', 'apps.registro.views.establecimiento.datos_establecimiento', name = 'establecimientoDatos'),
    url(r'^establecimiento/([0-9]+)/detalle$', 'apps.registro.views.establecimiento.detalle', name = 'establecimientoDetalle'),
    url(r'^establecimiento/([0-9]+)/revisar_jurisdiccion', 'apps.registro.views.establecimiento.revisar_jurisdiccion', name = 'establecimientoRevisarJurisdiccion'),
    url(r'^anexo$', 'apps.registro.views.anexo.index', name = 'anexo'),
    url(r'^anexo/([0-9]+)/edit', 'apps.registro.views.anexo.edit', name = 'anexoEdit'),
    url(r'^anexo/create', 'apps.registro.views.anexo.create', name = 'anexoCreate'),
    url(r'^anexo/([0-9]+)/baja', 'apps.registro.views.anexo.baja', name = 'anexoBaja'),
    url(r'^anexo/completar_datos_basicos/', 'apps.registro.views.anexo.completar_datos_basicos', name = 'anexoCompletarDatosBasicos'),
    url(r'^anexo/completar_turnos/', 'apps.registro.views.anexo.completar_turnos', name = 'anexoCompletarTurnos'),
    url(r'^anexo/completar_domicilio/', 'apps.registro.views.anexo.completar_domicilio', name = 'anexoCompletarDomicilio'),
    url(r'^unidad_extension$', 'apps.registro.views.unidad_extension.index', name = 'unidad_extension'),
    url(r'^unidad_extension/([0-9]+)/edit', 'apps.registro.views.unidad_extension.edit', name = 'unidadExtensionEdit'),
    url(r'^unidad_extension/create', 'apps.registro.views.unidad_extension.create', name = 'unidadExtensionCreate'),
    url(r'^unidad_extension/([0-9]+)/baja', 'apps.registro.views.unidad_extension.baja', name = 'unidadExtensionBaja'),
    url(r'^dependencia_funcional$', 'apps.registro.views.dependencia_funcional.index', name = 'dependenciaFuncional'),
    url(r'^dependencia_funcional/([0-9]+)/edit', 'apps.registro.views.dependencia_funcional.edit', name = 'dependenciaFuncionalEdit'),
    url(r'^dependencia_funcional/create', 'apps.registro.views.dependencia_funcional.create', name = 'dependenciaFuncionalCreate'),
    url(r'^dependencia_funcional/([0-9]+)/delete', 'apps.registro.views.dependencia_funcional.delete', name = 'dependenciaFuncionalDelete'),
    # AJAX
    url(r'^ajax/get_localidades_por_departamento/(?P<departamento_id>[0-9]+)', 'apps.registro.views.ajax.get_localidades_por_departamento', name = 'ajaxGetLocalidadesPorTipo'),
    url(r'^ajax/get_departamentos_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.registro.views.ajax.get_departamentos_por_jurisdiccion', name = 'ajaxGetDepartamentosPorJurisdiccion'),
   )
