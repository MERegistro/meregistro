# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^index$', 'apps.titulos.views.titulo.index', name = 'titulosHome'),
    url(r'^create', 'apps.titulos.views.titulo.create', name = 'tituloCreate'),
    url(r'^([0-9]+)/edit', 'apps.titulos.views.titulo.edit', name = 'tituloEdit'),
    url(r'^([0-9]+)/eliminar', 'apps.titulos.views.titulo.eliminar', name = 'tituloEliminar'),
    # Orientaciones
    url(r'^orientaciones/create', 'apps.titulos.views.orientacion.create', name = 'orientacionCreate'),
    url(r'^orientaciones/([0-9]+)/editar', 'apps.titulos.views.orientacion.edit', name = 'orientacionEdit'),
    url(r'^([0-9]+)/asignar-orientacion', 'apps.titulos.views.orientacion.create', name = 'orientacionCreate'),
    url(r'^([0-9]+)/orientaciones', 'apps.titulos.views.orientacion.orientaciones_por_titulo', name = 'orientacionesPorTitulo'),
    url(r'^orientaciones', 'apps.titulos.views.orientacion.index', name = 'orientaciones'),
    # Normativa jurisdiccional
    url(r'^normativa_jurisdiccional/create', 'apps.titulos.views.normativa_jurisdiccional.create', name = 'normativaJurisdiccionalCreate'),
    url(r'^normativa_jurisdiccional', 'apps.titulos.views.normativa_jurisdiccional.index', name = 'normativaJurisdiccional'),
)
