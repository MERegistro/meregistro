# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.consulta_validez.views.index', name='consultaValidezHome'),
    url(r'^([0-9]+)/detalle$', 'apps.consulta_validez.views.detalle', name='consultaValidezDetalle'),
    # AJAX
    url(r'^ajax/get_unidades_por_jurisdiccion/(?P<jurisdiccion_id>[0-9]+)', 'apps.consulta_validez.views.ajax_get_unidades_por_jurisdiccion', name='ajaxGetUnidadesPorJurisdiccion'),

    url(r'^ajax/get_carreras', 'apps.consulta_validez.views.ajax_get_carreras', name='ajaxGetCarreras'),
    url(r'^ajax/get_titulos', 'apps.consulta_validez.views.ajax_get_titulos', name='ajaxGetTitulos'),
)
