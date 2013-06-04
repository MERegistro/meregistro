# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns=patterns('',
    url(r'^solicitud$', 'apps.validez_nacional.views.solicitud.index', name='validezNacionalSolicitudIndex'),
    url(r'^solicitud/create$', 'apps.validez_nacional.views.solicitud.create', name='validezNacionalSolicitudCreate'),
    #url(r'^validez_nacional/([0-9]+)/editar$', 'apps.titulos.views.validez_nacional.edit', name='validezNacionalEdit'),
    #url(r'^validez_nacional/([0-9]+)/delete$', 'apps.titulos.views.validez_nacional.delete', name='validezNacionalEliminar'),
    url(r'^$', 'apps.validez_nacional.views.solicitud.index', name='validezNacionalIndex'),
    # AJAX
    url(r'^ajax/get_titulos_por_carrera/([0-9]+)', 'apps.validez_nacional.views.ajax.get_titulos_por_carrera', name='ajaxGetTitulosPorCarrera'),
    
)
