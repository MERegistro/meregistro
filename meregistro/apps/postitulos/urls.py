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
    url(r'^postitulo_nacional/create$', 'apps.postitulos.views.postitulo_nacional.create', name='postituloNacionalCreate'),
    url(r'^postitulo_nacional/([0-9]+)/editar$', 'apps.postitulos.views.postitulo_nacional.edit', name='postituloNacionalEdit'),
    url(r'^postitulo_nacional/([0-9]+)/eliminar$', 'apps.postitulos.views.postitulo_nacional.delete', name='postituloNacionalEliminar'),
    url(r'^postitulo_nacional$', 'apps.postitulos.views.postitulo_nacional.index', name='postituloNacional'),
    # Carrera jurisdiccional
    url(r'^carrera_jurisdiccional$', 'apps.postitulos.views.carrera_jurisdiccional.index', name='carreraJurisdiccional'),
    url(r'^carrera_jurisdiccional/create$', 'apps.postitulos.views.carrera_jurisdiccional.create', name='carreraJurisdiccionalCreate'),
    url(r'^carrera_jurisdiccional/([0-9]+)/edit$', 'apps.postitulos.views.carrera_jurisdiccional.edit', name='carreraJurisdiccionalEdit'),
    #url(r'^carrera_jurisdiccional/([0-9]+)/editar_normativas$', 'apps.titulos.views.carrera_jurisdiccional.editar_normativas', name='carreraJurisdiccionalNormativasEdit'),
    #url(r'^carrera_jurisdiccional/editar_normativas$', 'apps.titulos.views.carrera_jurisdiccional.editar_normativas', { 'carrera_jurisdiccional_id': None }, name='carreraJurisdiccionalNormativasEdit'),
    #url(r'^carrera_jurisdiccional/([0-9]+)/editar_cohortes$', 'apps.titulos.views.carrera_jurisdiccional.editar_cohortes', name='carreraJurisdiccionalCohortesEdit'),
    #url(r'^carrera_jurisdiccional/editar_cohortes$', 'apps.titulos.views.carrera_jurisdiccional.editar_cohortes', { 'carrera_jurisdiccional_id': None }, name='carreraJurisdiccionalCohortesEdit'),
    #url(r'^carrera_jurisdiccional/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.carrera_jurisdiccional.revisar_jurisdiccion', name='carreraJurisdiccionalRevisarJurisdiccion'),
    #url(r'^carrera_jurisdiccional/([0-9]+)/eliminar$', 'apps.titulos.views.carrera_jurisdiccional.eliminar', name='carreraJurisdiccionalEliminar'),
)
