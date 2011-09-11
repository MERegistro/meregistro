# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^index$', 'apps.titulos.views.titulo.index', name = 'titulosHome'),
    url(r'^create$', 'apps.titulos.views.titulo.create', name = 'tituloCreate'),
    url(r'^([0-9]+)/edit$', 'apps.titulos.views.titulo.edit', name = 'tituloEdit'),
    url(r'^([0-9]+)/eliminar$', 'apps.titulos.views.titulo.eliminar', name = 'tituloEliminar'),
    # Orientaciones
    url(r'^orientaciones/create$', 'apps.titulos.views.orientacion.create', name = 'orientacionCreate'),
    url(r'^orientaciones/([0-9]+)/editar$', 'apps.titulos.views.orientacion.edit', name = 'orientacionEdit'),
    url(r'^([0-9]+)/asignar-orientacion$', 'apps.titulos.views.orientacion.create', name = 'orientacionCreate'),
    url(r'^([0-9]+)/orientaciones$', 'apps.titulos.views.orientacion.orientaciones_por_titulo', name = 'orientacionesPorTitulo'),
    url(r'^orientaciones/([0-9]+)/eliminar$', 'apps.titulos.views.orientacion.eliminar', name = 'orientacionEliminar'),
    url(r'^orientaciones$', 'apps.titulos.views.orientacion.index', name = 'orientaciones'),
    # Normativa jurisdiccional
    url(r'^normativa_jurisdiccional/create$', 'apps.titulos.views.normativa_jurisdiccional.create', name = 'normativaJurisdiccionalCreate'),
    url(r'^normativa_jurisdiccional/([0-9]+)/editar$', 'apps.titulos.views.normativa_jurisdiccional.edit', name = 'normativaJurisdiccionalEdit'),
    url(r'^normativa_jurisdiccional/([0-9]+)/eliminar$', 'apps.titulos.views.normativa_jurisdiccional.eliminar', name = 'normativaJurisdiccionalEliminar'),
    url(r'^normativa_jurisdiccional$', 'apps.titulos.views.normativa_jurisdiccional.index', name = 'normativaJurisdiccional'),
    # Matriculas
    url(r'^matricula/create$', 'apps.titulos.views.matricula.create', name = 'matriculaCreate'),
    url(r'^matricula/([0-9]+)/editar$', 'apps.titulos.views.matricula.edit', name = 'matriculaEdit'),
    url(r'^matricula/([0-9]+)/delete$', 'apps.titulos.views.matricula.delete', name = 'matriculaDelete'),
    url(r'^matricula$', 'apps.titulos.views.matricula.index', name = 'matricula'),
    # Proyecto
    url(r'^proyecto/create$', 'apps.titulos.views.proyecto.create', name = 'proyectoCreate'),
    url(r'^proyecto/([0-9]+)/editar$', 'apps.titulos.views.proyecto.edit', name = 'proyectoEdit'),
    url(r'^proyecto/([0-9]+)/delete$', 'apps.titulos.views.proyecto.delete', name = 'proyectoDelete'),
    url(r'^proyecto$', 'apps.titulos.views.proyecto.index', name = 'proyecto'),
    # Título jurisdiccional
    url(r'^titulo_jurisdiccional/create$', 'apps.titulos.views.titulo_jurisdiccional.create', name = 'tituloJurisdiccionalCreate'),
    url(r'^titulo_jurisdiccional/([0-9]+)/orientaciones$', 'apps.titulos.views.titulo_jurisdiccional.orientaciones_por_titulo', name = 'orientacionesPorTituloJurisdiccional'),
    url(r'^titulo_jurisdiccional/([0-9]+)/editar_orientaciones$', 'apps.titulos.views.titulo_jurisdiccional.editar_orientaciones', name = 'tituloJurisdiccionalOrientacionesEdit'),
    url(r'^titulo_jurisdiccional/editar_orientaciones$', 'apps.titulos.views.titulo_jurisdiccional.editar_orientaciones', { 'titulo_jurisdiccional_id': None }, name = 'tituloJurisdiccionalOrientacionesEdit'),
    url(r'^titulo_jurisdiccional/([0-9]+)/editar_modalidades$', 'apps.titulos.views.titulo_jurisdiccional.editar_modalidades', name = 'tituloJurisdiccionalModalidadesEdit'),
    url(r'^titulo_jurisdiccional/editar_modalidades$', 'apps.titulos.views.titulo_jurisdiccional.editar_modalidades', { 'titulo_jurisdiccional_id': None }, name = 'tituloJurisdiccionalModalidadesEdit'),
    url(r'^titulo_jurisdiccional/([0-9]+)/editar_normativas$', 'apps.titulos.views.titulo_jurisdiccional.editar_normativas', name = 'tituloJurisdiccionalNormativasEdit'),
    url(r'^titulo_jurisdiccional/editar_normativas$', 'apps.titulos.views.titulo_jurisdiccional.editar_normativas', { 'titulo_jurisdiccional_id': None }, name = 'tituloJurisdiccionalNormativasEdit'),
    url(r'^titulo_jurisdiccional/([0-9]+)/editar_cohortes$', 'apps.titulos.views.titulo_jurisdiccional.editar_cohortes', name = 'tituloJurisdiccionalCohortesEdit'),
    url(r'^titulo_jurisdiccional/editar_cohortes$', 'apps.titulos.views.titulo_jurisdiccional.editar_cohortes', { 'titulo_jurisdiccional_id': None }, name = 'tituloJurisdiccionalCohortesEdit'),
    url(r'^titulo_jurisdiccional/([0-9]+)/edit$', 'apps.titulos.views.titulo_jurisdiccional.edit', name = 'tituloJurisdiccionalEdit'),
    url(r'^titulo_jurisdiccional$', 'apps.titulos.views.titulo_jurisdiccional.index', name = 'tituloJurisdiccional'),
    # Cohorte
    url(r'^cohorte/create$', 'apps.titulos.views.cohorte.create', { 'titulo_jurisdiccional_id': None }, name = 'cohorteCreate'),
    url(r'^cohorte/([0-9]+)/editar$', 'apps.titulos.views.cohorte.edit', name = 'cohorteEdit'),
    url(r'^titulo_jurisdiccional/([0-9]+)/asignar-cohorte$', 'apps.titulos.views.cohorte.create', name = 'cohorteCreate'),
    url(r'^titulo_jurisdiccional/([0-9]+)/cohortes$', 'apps.titulos.views.cohorte.cohortes_por_titulo', name = 'cohortesPorTitulo'),
    url(r'^cohorte/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte.eliminar', name = 'cohorteEliminar'),
    url(r'^cohorte/([0-9]+)/asignar-establecimientos$', 'apps.titulos.views.cohorte.asignar_establecimientos', name = 'cohorteAsignarEstablecimientos'),
    url(r'^cohorte/([0-9]+)/asignar-anexos$', 'apps.titulos.views.cohorte.asignar_anexos', name = 'cohorteAsignarAnexos'),
    url(r'^cohorte/([0-9]+)/asignar-unidades-extension$', 'apps.titulos.views.cohorte.asignar_unidades_extension', name = 'cohorteAsignarUnidadesExtension'),
    url(r'^cohorte$', 'apps.titulos.views.cohorte.index', name = 'cohorte'),
    # Cohorte establecimiento
    url(r'^cohorte-establecimiento/([0-9]+)/confirmar$', 'apps.titulos.views.cohorte_establecimiento.confirmar', name = 'cohorteEstablecimientoConfirmar'),
    url(r'^cohorte-establecimiento$', 'apps.titulos.views.cohorte_establecimiento.index', name = 'cohorteEstablecimientoIndex'),
    url(r'^cohorte-establecimiento/([0-9]+)/seguimiento$', 'apps.titulos.views.cohorte_establecimiento.seguimiento', name = 'cohorteEstablecimientoSeguimiento'),
    url(r'^cohorte-establecimiento/([0-9]+)/editar-seguimiento$', 'apps.titulos.views.cohorte_establecimiento.edit_seguimiento', name = 'cohorteEstablecimientoSeguimientoCreate'),
    url(r'^cohorte-establecimiento/([0-9]+)/crear-seguimiento$', 'apps.titulos.views.cohorte_establecimiento.create_seguimiento', name = 'cohorteEstablecimientoSeguimientoEdit'),
    url(r'^cohorte-establecimiento/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte_establecimiento.eliminar', name = 'cohorteEstablecimientoSeguimientoEliminar'),
    # Cohorte anexo
    url(r'^cohorte-anexo/([0-9]+)/confirmar$', 'apps.titulos.views.cohorte_anexo.confirmar', name = 'cohorteAnexoConfirmar'),
    url(r'^cohorte-anexo$', 'apps.titulos.views.cohorte_anexo.index', name = 'cohorteAnexoIndex'),
    url(r'^cohorte-anexo/([0-9]+)/seguimiento$', 'apps.titulos.views.cohorte_anexo.seguimiento', name = 'cohorteAnexoSeguimiento'),
    url(r'^cohorte-anexo/([0-9]+)/editar-seguimiento$', 'apps.titulos.views.cohorte_anexo.edit_seguimiento', name = 'cohorteAnexoSeguimientoCreate'),
    url(r'^cohorte-anexo/([0-9]+)/crear-seguimiento$', 'apps.titulos.views.cohorte_anexo.create_seguimiento', name = 'cohorteAnexoSeguimientoEdit'),
    url(r'^cohorte-anexo/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte_anexo.eliminar', name = 'cohorteAnexoSeguimientoEliminar'),
    # AJAX
    url(r'^ajax/get_titulos_por_tipo/(?P<tipo_titulo_id>[0-9]+)', 'apps.titulos.views.ajax.get_titulos_por_tipo', name = 'ajaxGetTitulosPorTipo'),
    url(r'^ajax/get_rango_anios_cohorte/(?P<titulo_jurisdiccional_id>[0-9]+)', 'apps.titulos.views.ajax.get_rango_anios_cohorte', name = 'ajaxGetRangoAniosCohorte'),
    # Proyecto
    url(r'^postitulo/create$', 'apps.titulos.views.postitulo.create', name = 'postituloCreate'),
    url(r'^postitulo/([0-9]+)/editar$', 'apps.titulos.views.postitulo.edit', name = 'postituloEdit'),
    url(r'^postitulo/([0-9]+)/delete$', 'apps.titulos.views.postitulo.delete', name = 'postituloDelete'),
    url(r'^postitulo$', 'apps.titulos.views.postitulo.index', name = 'postitulo'),
)
