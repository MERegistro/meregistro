# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^(?P<anio>[0-9]{4})$', 'apps.oferta_nacional.views.index', name='ofertaNacionalHome'),
    # AJAX
    url(r'^ajax/get_establecimientos_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.oferta_nacional.views.ajax_get_establecimientos_por_jurisdiccion', name='ajaxGetEstablecimientosPorJurisdiccion'),
    url(r'^ajax/get_establecimientos_por_jurisdiccion/', 'apps.oferta_nacional.views.ajax_get_establecimientos_por_jurisdiccion', { 'jurisdiccion_id': 0 }, name='ajaxGetEstablecimientosPorJurisdiccion'),
    
    url(r'^ajax/get_carreras_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.oferta_nacional.views.ajax_get_carreras_por_jurisdiccion', name='ajaxGetCarrerasPorJurisdiccion'),
    url(r'^ajax/get_carreras_por_jurisdiccion/', 'apps.oferta_nacional.views.ajax_get_carreras_por_jurisdiccion', { 'jurisdiccion_id': 0 }, name='ajaxGetCarrerasPorJurisdiccion'),
    
    url(r'^ajax/get_carreras_por_establecimiento/(?P<establecimiento_id>[0-9]+)', 'apps.oferta_nacional.views.ajax_get_carreras_por_establecimiento', name='ajaxGetCarrerasPorEstablecimiento'),
    url(r'^ajax/get_carreras_por_establecimiento/', 'apps.oferta_nacional.views.ajax_get_carreras_por_establecimiento', { 'establecimiento_id': 0 }, name='ajaxGetCarrerasPorEstablecimiento'),
)
