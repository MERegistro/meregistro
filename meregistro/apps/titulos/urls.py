# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^index$', 'apps.titulos.views.titulo.index', name = 'titulosHome'),
    url(r'^create', 'apps.titulos.views.titulo.create', name = 'tituloCreate'),
    url(r'^([0-9]+)/edit', 'apps.titulos.views.titulo.edit', name = 'tituloEdit'),
    url(r'^([0-9]+)/baja', 'apps.titulos.views.titulo.baja', name = 'tituloBaja'),
    #url(r'^([0-9]+)/orientaciones', 'apps.titulos.views.titulo.baja', name = 'tituloOrientaciones'),
)
