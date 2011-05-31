# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'registro.views.index', name = 'home'),
    url(r'^establecimiento$', 'registro.views.establecimiento.index', name = 'establecimiento'),
    url(r'^establecimiento/([0-9]+)/edit', 'registro.views.establecimiento.edit', name = 'establecimientoEdit'),
    url(r'^establecimiento/create', 'registro.views.establecimiento.create', name = 'establecimientoCreate'),
    url(r'^establecimiento/([0-9]+)/delete', 'registro.views.establecimiento.delete', name = 'establecimientoDelete'),
    url(r'^establecimiento/completar_datos/', 'registro.views.establecimiento.completar_datos', name = 'establecimientoCompletarDatos'),
    url(r'^establecimiento/completar_datos_basicos/', 'registro.views.establecimiento.completar_datos_basicos', name = 'establecimientoCompletarDatosBasicos'),
    url(r'^establecimiento/completar_niveles/', 'registro.views.establecimiento.completar_niveles', name = 'establecimientoCompletarNiveles'),
    url(r'^establecimiento/completar_turnos/', 'registro.views.establecimiento.completar_turnos', name = 'establecimientoCompletarTurnos'),
    url(r'^establecimiento/completar_funciones/', 'registro.views.establecimiento.completar_funciones', name = 'establecimientoCompletarFunciones'),
    url(r'^establecimiento/completar_domicilio/', 'registro.views.establecimiento.completar_domicilio', name = 'establecimientoCompletarDomicilio'),
    url(r'^establecimiento/completar_informacion_edilicia/', 'registro.views.establecimiento.completar_informacion_edilicia', name = 'establecimientoCompletarInformacionEdilicia'),
    url(r'^establecimiento/([0-9]+)/registrar', 'registro.views.establecimiento.registrar', name = 'establecimientoRegistrar'),
    url(r'^anexo$', 'registro.views.anexo.index', name = 'anexo'),
    url(r'^anexo/([0-9]+)/edit', 'registro.views.anexo.edit', name = 'anexoEdit'),
    url(r'^anexo/create', 'registro.views.anexo.create', name = 'anexoCreate'),
    url(r'^unidad_extension$', 'registro.views.unidad_extension.index', name = 'unidad_extension'),
    url(r'^unidad_extension/([0-9]+)/edit', 'registro.views.unidad_extension.edit', name = 'unidadExtensionEdit'),
    url(r'^unidad_extension/create', 'registro.views.unidad_extension.create', name = 'unidadExtensionCreate'),
    url(r'^dependencia_funcional$', 'registro.views.dependencia_funcional.index', name = 'dependenciaFuncional'),
    url(r'^dependencia_funcional/([0-9]+)/edit', 'registro.views.dependencia_funcional.edit', name = 'dependenciaFuncionalEdit'),
    url(r'^dependencia_funcional/create', 'registro.views.dependencia_funcional.create', name = 'dependenciaFuncionalCreate'),
    url(r'^dependencia_funcional/([0-9]+)/delete', 'registro.views.dependencia_funcional.delete', name = 'dependenciaFuncionalDelete'),
)
