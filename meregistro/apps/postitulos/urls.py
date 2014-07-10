# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns=patterns('',
    # Carrera
    url(r'^carrera/create$', 'apps.postitulos.views.carrera.create', name='carreraPostituloCreate'),
    url(r'^carrera/([0-9]+)/editar$', 'apps.postitulos.views.carrera.edit', name='carreraPostituloEdit'),
    url(r'^carrera/([0-9]+)/delete$', 'apps.postitulos.views.carrera.delete', name='carreraPostituloEliminar'),
    url(r'^carrera/([0-9]+)/postitulos$', 'apps.postitulos.views.carrera.postitulos', name='carreraPostituloPostitulos'),
    url(r'^carrera$', 'apps.postitulos.views.carrera.index', name='carreraPostitulos'),
    # Normativas
    url(r'^normativa/create$', 'apps.postitulos.views.normativa.create', name='normativaPostituloCreate'),
    url(r'^normativa/([0-9]+)/editar$', 'apps.postitulos.views.normativa.edit', name='normativaPostituloEdit'),
    url(r'^normativa/([0-9]+)/eliminar$', 'apps.postitulos.views.normativa.delete', name='normativaPostituloEliminar'),
    url(r'^normativa$', 'apps.postitulos.views.normativa.index', name='normativaPostitulo'),
    # Títulos nacionales
    url(r'^postitulo_nacional/create$', 'apps.postitulos.views.postitulo_nacional.create', name='postituloNacionalCreate'),
    url(r'^postitulo_nacional/([0-9]+)/editar$', 'apps.postitulos.views.postitulo_nacional.edit', name='postituloNacionalEdit'),
    url(r'^postitulo_nacional/([0-9]+)/eliminar$', 'apps.postitulos.views.postitulo_nacional.delete', name='postituloNacionalEliminar'),
    url(r'^postitulo_nacional$', 'apps.postitulos.views.postitulo_nacional.index', name='postituloNacional'),
    # Carrera jurisdiccional
    url(r'^carrera_jurisdiccional$', 'apps.postitulos.views.carrera_jurisdiccional.index', name='carreraPostituloJurisdiccional'),
    url(r'^carrera_jurisdiccional/create$', 'apps.postitulos.views.carrera_jurisdiccional.create', name='carreraPostituloJurisdiccionalCreate'),
    url(r'^carrera_jurisdiccional/([0-9]+)/edit$', 'apps.postitulos.views.carrera_jurisdiccional.edit', name='carreraPostituloJurisdiccionalEdit'),
    url(r'^carrera_jurisdiccional/([0-9]+)/eliminar$', 'apps.postitulos.views.carrera_jurisdiccional.eliminar', name='carreraPostituloJurisdiccionalEliminar'),
    # Normativa jurisdiccional
    url(r'^normativa_jurisdiccional/create$', 'apps.postitulos.views.normativa_jurisdiccional.create', name='normativaPostituloJurisdiccionalCreate'),
    url(r'^normativa_jurisdiccional/([0-9]+)/editar$', 'apps.postitulos.views.normativa_jurisdiccional.edit', name='normativaPostituloJurisdiccionalEdit'),
    url(r'^normativa_jurisdiccional/([0-9]+)/eliminar$', 'apps.postitulos.views.normativa_jurisdiccional.eliminar', name='normativaPostituloJurisdiccionalEliminar'),
    url(r'^normativa_jurisdiccional$', 'apps.postitulos.views.normativa_jurisdiccional.index', name='normativaPostituloJurisdiccional'),
    #url(r'^normativa_jurisdiccional/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.normativa_jurisdiccional.revisar_jurisdiccion', name='normativaJurisdiccionalRevisarJurisdiccion'),
    url(r'^solicitud$', 'apps.postitulos.views.solicitud.index', name='postituloSolicitudIndex'),
    url(r'^solicitud/([0-9]+)/eliminar$', 'apps.postitulos.views.solicitud.delete', name='postitulosSolicitudEdit'),
    url(r'^solicitud/create$', 'apps.postitulos.views.solicitud.create', name='postituloSolicitudCreate'),
    url(r'^solicitud/([0-9]+)/editar$', 'apps.postitulos.views.solicitud.edit', name='postituloSolicitudEdit'),
    url(r'^solicitud/([0-9]+)/editar_normativas$', 'apps.postitulos.views.solicitud.editar_normativas', name='postituloSolicitudNormativasEdit'),
    url(r'^solicitud/editar_normativas$', 'apps.postitulos.views.solicitud.editar_normativas', { 'solicitud_id': None }, name='postituloSolicitudNormativasEdit'),
    url(r'^solicitud/([0-9]+)/editar_cohortes$', 'apps.postitulos.views.solicitud.editar_cohortes', name='postituloSolicitudCohortesEdit'),
    url(r'^solicitud/editar_cohortes$', 'apps.postitulos.views.solicitud.editar_cohortes', { 'solicitud_id': None }, name='postituloSolicitudCohortesEdit'),
    url(r'^solicitud/([0-9]+)/asignar-establecimientos$', 'apps.postitulos.views.solicitud.asignar_establecimientos', name='postituloSolicitudAsignarEstablecimientos'),
    url(r'^solicitud/([0-9]+)/asignar-anexos$', 'apps.postitulos.views.solicitud.asignar_anexos', name='postituloSolicitudAsignarAnexos'),
    url(r'^solicitud/([0-9]+)/control$', 'apps.postitulos.views.solicitud.control', name='postituloSolicitudControl'),
    url(r'^solicitud/([0-9]+)/numerar$', 'apps.postitulos.views.solicitud.numerar', name='postituloSolicitudNumerar'),
    url(r'^solicitud/([0-9]+)/detalle-numeracion/([0-9]+)$', 'apps.postitulos.views.solicitud.detalle_numeracion', name='postituloSolicitudDetalleNumeracion'),
    # Validez Nacional
    url(r'^validez$', 'apps.postitulos.views.validez.index', name='postituloValidezNacionalIndex'),
    url(r'^validez/([0-9]+)/editar$', 'apps.postitulos.views.validez.edit', name='postituloValidezNacionalEditarValidez'),
    url(r'^validez/([0-9]+)/eliminar$', 'apps.postitulos.views.validez.eliminar', name='postituloValidezNacionalEliminar'),
    # AJAX
    url(r'^ajax/get_postitulos_por_carrera/([0-9]?)', 'apps.postitulos.views.ajax.get_postitulos_por_carrera', name='ajaxGetPostitulosPorCarrera'),
    #url(r'^ajax/chequear_nro_infd/([0-9]+)/([0-9a-zA-Z]+)', 'apps.validez_nacional.views.ajax.chequear_nro_infd', name='ajaxChequearNroINFD'),
      
    )
