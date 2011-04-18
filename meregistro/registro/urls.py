# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'registro.views.index', name = 'home'),
    url(r'^establecimiento$', 'registro.views.establecimiento.index', name = 'establecimiento'),
    url(r'^establecimiento/([0-9]+)/edit', 'registro.views.establecimiento.edit', name = 'establecimientoEdit'),
    url(r'^establecimiento/create', 'registro.views.establecimiento.create', name = 'establecimientoCreate'),
    url(r'^anexo$', 'registro.views.anexo.index', name = 'anexo'),
    url(r'^anexo/([0-9]+)/edit', 'registro.views.anexo.edit', name = 'anexoEdit'),
    url(r'^anexo/create', 'registro.views.anexo.create', name = 'anexoCreate'),
    url(r'^dependencia_funcional$', 'registro.views.dependencia_funcional.index', name = 'dependenciaFuncional'),
    url(r'^dependencia_funcional/([0-9]+)/edit', 'registro.views.dependencia_funcional.edit', name = 'dependenciaFuncionalEdit'),
    url(r'^dependencia_funcional/create', 'registro.views.dependencia_funcional.create', name = 'dependenciaFuncionalCreate'),
)
