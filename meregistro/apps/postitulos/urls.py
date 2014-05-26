# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns=patterns('',
    # Carrera
    url(r'^carrera/create$', 'apps.postitulos.views.carrera.create', name='carreraCreate'),
    url(r'^carrera/([0-9]+)/editar$', 'apps.postitulos.views.carrera.edit', name='carreraEdit'),
    url(r'^carrera/([0-9]+)/delete$', 'apps.postitulos.views.carrera.delete', name='carreraEliminar'),
    url(r'^carrera/([0-9]+)/postitulos$', 'apps.postitulos.views.carrera.postitulos', name='carreraPostitulos'),
    url(r'^carrera$', 'apps.postitulos.views.carrera.index', name='carrera'),
    # Normativas
    url(r'^normativa/create$', 'apps.postitulos.views.normativa.create', name='normativaCreate'),
    url(r'^normativa/([0-9]+)/editar$', 'apps.postitulos.views.normativa.edit', name='normativaPostituloEdit'),
    url(r'^normativa/([0-9]+)/eliminar$', 'apps.postitulos.views.normativa.delete', name='normativaPostituloEliminar'),
    url(r'^normativa$', 'apps.postitulos.views.normativa.index', name='normativaPostitulo'),
    # Títulos nacionales
    #url(r'^postitulo/create$', 'apps.postitulos.views.postitulo_nacional.create', name='postituloNacionalCreate'),
    #url(r'^postitulo/([0-9]+)/editar$', 'apps.titulos.views.titulo_nacional.edit', name='tituloNacionalEdit'),
    #url(r'^titulo_nacional/([0-9]+)/eliminar$', 'apps.titulos.views.titulo_nacional.delete', name='tituloNacionalEliminar'),
    url(r'^postitulo_nacional$', 'apps.postitulos.views.postitulo_nacional.index', name='postituloNacional'),
)
