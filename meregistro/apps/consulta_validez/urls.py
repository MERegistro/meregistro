# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.consulta_validez.views.index', name='consultaValidezHome'),
    url(r'^([0-9]+)/detalle$', 'apps.consulta_validez.views.detalle', name='consultaValidezDetalle'),
    # AJAX
    url(r'^ajax/get_unidades_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_unidades_por_jurisdiccion', name='ajaxGetUnidadesPorJurisdiccion'),
    url(r'^ajax/get_carreras_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_carreras_por_jurisdiccion', name='ajaxGetCarrerasPorJurisdiccion'),
    url(r'^ajax/get_titulos_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_titulos_por_jurisdiccion', name='ajaxGetTitulosPorJurisdiccion'),
   
    url(r'^ajax/get_carreras_por_ue/(?P<ue_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_carreras_por_ue', name='ajaxGetCarrerasPorUe'),
    url(r'^ajax/get_titulos_por_ue/(?P<ue_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_titulos_por_ue', name='ajaxGetTitulosPorUe'),
 
    url(r'^ajax/get_titulos_por_carrera/(?P<carrera_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_titulos_por_carrera', name='ajaxGetTitulosPorCarrera'),

)
