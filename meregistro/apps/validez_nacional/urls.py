# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns=patterns('',
    url(r'^solicitud$', 'apps.validez_nacional.views.solicitud.index', name='validezNacionalSolicitudIndex'),
    url(r'^solicitud/create$', 'apps.validez_nacional.views.solicitud.create', name='validezNacionalSolicitudCreate'),
    url(r'^solicitud/([0-9]+)/editar$', 'apps.validez_nacional.views.solicitud.edit', name='validezNacionalSolicitudEdit'),
    url(r'^solicitud/([0-9]+)/eliminar$', 'apps.validez_nacional.views.solicitud.delete', name='validezNacionalSolicitudEdit'),
    url(r'^solicitud/consulta_institucional$', 'apps.validez_nacional.views.solicitud.consulta_institucional', name='validezNacionalConsultaInstitucional'),
    #url(r'^validez_nacional/([0-9]+)/delete$', 'apps.titulos.views.validez_nacional.delete', name='validezNacionalEliminar'),
    url(r'^$', 'apps.validez_nacional.views.solicitud.index', name='validezNacionalIndex'),
    # Normativa jurisdiccional
    url(r'^solicitud/([0-9]+)/editar_normativas$', 'apps.validez_nacional.views.solicitud.editar_normativas', name='solicitudNormativasEdit'),
    url(r'^solicitud/editar_normativas$', 'apps.validez_nacional.views.solicitud.editar_normativas', { 'solicitud_id': None }, name='solicitudNormativasEdit'),
    # Cohortes
    url(r'^solicitud/([0-9]+)/editar_cohortes$', 'apps.validez_nacional.views.solicitud.editar_cohortes', name='solicitudCohortesEdit'),
    url(r'^solicitud/editar_cohortes$', 'apps.validez_nacional.views.solicitud.editar_cohortes', { 'solicitud_id': None }, name='solicitudCohortesEdit'),
    # Control
    url(r'^solicitud/([0-9]+)/control$', 'apps.validez_nacional.views.solicitud.control', name='solicitudControl'),
    # Asignar establecimientos
    url(r'^solicitud/([0-9]+)/asignar-establecimientos$', 'apps.validez_nacional.views.solicitud.asignar_establecimientos', name='solicitudAsignarEstablecimientos'),
    # Asignar anexos
    url(r'^solicitud/([0-9]+)/asignar-anexos$', 'apps.validez_nacional.views.solicitud.asignar_anexos', name='solicitudAsignarAnexos'),
    # Numerar
    url(r'^solicitud/([0-9]+)/numerar$', 'apps.validez_nacional.views.solicitud.numerar', name='validezNacionalSolicitudNumerar'),
    # Validez Nacional
    url(r'^validez$', 'apps.validez_nacional.views.validez.index', name='validezNacionalIndex'),
    url(r'^validez/([0-9]+)/editar$', 'apps.validez_nacional.views.validez.edit', name='validezNacionalEditarValidez'),
    # AJAX
    url(r'^ajax/get_titulos_por_carrera/([0-9]+)', 'apps.validez_nacional.views.ajax.get_titulos_por_carrera', name='ajaxGetTitulosPorCarrera'),
    url(r'^ajax/chequear_nro_infd/([0-9]+)/([0-9a-zA-Z]+)', 'apps.validez_nacional.views.ajax.chequear_nro_infd', name='ajaxChequearNroINFD'),
    
)
