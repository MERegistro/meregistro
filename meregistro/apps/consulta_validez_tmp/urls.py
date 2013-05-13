# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.consulta_validez_tmp.views.index', name='consultaValidezTmpHome'),
    url(r'^([0-9]+)/detalle$', 'apps.consulta_validez_tmp.views.detalle', name='consultaValidezTmpDetalle'),
    # AJAX
    url(r'^ajax/get_unidades_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.consulta_validez_tmp.views.ajax_get_unidades_por_jurisdiccion', name='ajaxGetUnidadesPorJurisdiccion'),
    
    url(r'^ajax/get_unidades_por_tipo_gestion/$', 'apps.consulta_validez_tmp.views.ajax_get_unidades_por_tipo_gestion', { 'tipo_gestion_id': '0' }, name='ajaxGetUnidadesPorTipoGestionTodas'),
    url(r'^ajax/get_unidades_por_tipo_gestion/(?P<tipo_gestion_id>[0-9]+)', 'apps.consulta_validez_tmp.views.ajax_get_unidades_por_tipo_gestion', name='ajaxGetUnidadesPorTipoGestion'),
    
    url(r'^ajax/get_carreras', 'apps.consulta_validez_tmp.views.ajax_get_carreras', name='ajaxGetCarreras'),
    url(r'^ajax/get_titulos', 'apps.consulta_validez_tmp.views.ajax_get_titulos', name='ajaxGetTitulos'),
)
