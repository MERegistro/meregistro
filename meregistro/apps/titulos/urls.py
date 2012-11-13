# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns=patterns('',
    url(r'^index$', 'apps.titulos.views.titulo.index', name='titulosHome'),
    url(r'^create$', 'apps.titulos.views.titulo.create', name='tituloCreate'),
    url(r'^([0-9]+)/edit$', 'apps.titulos.views.titulo.edit', name='tituloEdit'),
    url(r'^([0-9]+)/eliminar$', 'apps.titulos.views.titulo.eliminar', name='tituloEliminar'),
    # Títulos nacionales
    url(r'^titulo_nacional/create$', 'apps.titulos.views.titulo_nacional.create', name='tituloNacionalCreate'),
    url(r'^titulo_nacional/([0-9]+)/editar$', 'apps.titulos.views.titulo_nacional.edit', name='tituloNacionalEdit'),
    url(r'^titulo_nacional/([0-9]+)/eliminar$', 'apps.titulos.views.titulo_nacional.delete', name='tituloNacionalEliminar'),
    url(r'^titulo_nacional$', 'apps.titulos.views.titulo_nacional.index', name='tituloNacional'),
    # Orientaciones
    url(r'^orientaciones/create$', 'apps.titulos.views.orientacion.create', name='orientacionCreate'),
    url(r'^orientaciones/([0-9]+)/editar$', 'apps.titulos.views.orientacion.edit', name='orientacionEdit'),
    url(r'^([0-9]+)/asignar-orientacion$', 'apps.titulos.views.orientacion.create', name='orientacionCreate'),
    url(r'^([0-9]+)/orientaciones$', 'apps.titulos.views.orientacion.orientaciones_por_titulo', name='orientacionesPorTitulo'),
    url(r'^orientaciones/([0-9]+)/eliminar$', 'apps.titulos.views.orientacion.eliminar', name='orientacionEliminar'),
    url(r'^orientaciones$', 'apps.titulos.views.orientacion.index', name='orientaciones'),
    # Normativa jurisdiccional
    url(r'^normativa_jurisdiccional/create$', 'apps.titulos.views.normativa_jurisdiccional.create', name='normativaJurisdiccionalCreate'),
    url(r'^normativa_jurisdiccional/([0-9]+)/editar$', 'apps.titulos.views.normativa_jurisdiccional.edit', name='normativaJurisdiccionalEdit'),
    url(r'^normativa_jurisdiccional/([0-9]+)/eliminar$', 'apps.titulos.views.normativa_jurisdiccional.eliminar', name='normativaJurisdiccionalEliminar'),
    url(r'^normativa_jurisdiccional$', 'apps.titulos.views.normativa_jurisdiccional.index', name='normativaJurisdiccional'),
    url(r'^normativa_jurisdiccional/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.normativa_jurisdiccional.revisar_jurisdiccion', name='normativaJurisdiccionalRevisarJurisdiccion'),
    # Normativa nacional
    url(r'^normativa_nacional/create$', 'apps.titulos.views.normativa_nacional.create', name='normativaNacionalCreate'),
    url(r'^normativa_nacional/([0-9]+)/editar$', 'apps.titulos.views.normativa_nacional.edit', name='normativaNacionalEdit'),
    url(r'^normativa_nacional/([0-9]+)/eliminar$', 'apps.titulos.views.normativa_nacional.delete', name='normativaNacionalEliminar'),
    url(r'^normativa_nacional$', 'apps.titulos.views.normativa_nacional.index', name='normativaNacional'),
    # Matriculas
    url(r'^matricula/create$', 'apps.titulos.views.matricula.create', name='matriculaCreate'),
    url(r'^matricula/([0-9]+)/editar$', 'apps.titulos.views.matricula.edit', name='matriculaEdit'),
    url(r'^matricula/([0-9]+)/delete$', 'apps.titulos.views.matricula.delete', name='matriculaDelete'),
    url(r'^matricula$', 'apps.titulos.views.matricula.index', name='matricula'),
    url(r'^matricula/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.matricula.revisar_jurisdiccion', name='matriculaRevisarJurisdiccion'),
    # Proyecto
    url(r'^proyecto/create$', 'apps.titulos.views.proyecto.create', name='proyectoCreate'),
    url(r'^proyecto/([0-9]+)/editar$', 'apps.titulos.views.proyecto.edit', name='proyectoEdit'),
    url(r'^proyecto/([0-9]+)/delete$', 'apps.titulos.views.proyecto.delete', name='proyectoDelete'),
    url(r'^proyecto$', 'apps.titulos.views.proyecto.index', name='proyecto'),
    # Carrera jurisdiccional
    url(r'^carrera_jurisdiccional/create$', 'apps.titulos.views.carrera_jurisdiccional.create', name='carreraJurisdiccionalCreate'),
    url(r'^carrera_jurisdiccional/([0-9]+)/orientaciones$', 'apps.titulos.views.carrera_jurisdiccional.orientaciones_por_titulo', name='orientacionesPorCarreraJurisdiccional'),
    url(r'^carrera_jurisdiccional/([0-9]+)/editar_orientaciones$', 'apps.titulos.views.carrera_jurisdiccional.editar_orientaciones', name='carreraJurisdiccionalOrientacionesEdit'),
    url(r'^carrera_jurisdiccional/editar_orientaciones$', 'apps.titulos.views.carrera_jurisdiccional.editar_orientaciones', { 'carrera_jurisdiccional_id': None }, name='carreraJurisdiccionalOrientacionesEdit'),
    url(r'^carrera_jurisdiccional/([0-9]+)/editar_normativas$', 'apps.titulos.views.carrera_jurisdiccional.editar_normativas', name='carreraJurisdiccionalNormativasEdit'),
    url(r'^carrera_jurisdiccional/editar_normativas$', 'apps.titulos.views.carrera_jurisdiccional.editar_normativas', { 'carrera_jurisdiccional_id': None }, name='carreraJurisdiccionalNormativasEdit'),
    url(r'^carrera_jurisdiccional/([0-9]+)/editar_cohortes$', 'apps.titulos.views.carrera_jurisdiccional.editar_cohortes', name='carreraJurisdiccionalCohortesEdit'),
    url(r'^carrera_jurisdiccional/editar_cohortes$', 'apps.titulos.views.carrera_jurisdiccional.editar_cohortes', { 'carrera_jurisdiccional_id': None }, name='carreraJurisdiccionalCohortesEdit'),
    url(r'^carrera_jurisdiccional/([0-9]+)/edit$', 'apps.titulos.views.carrera_jurisdiccional.edit', name='carreraJurisdiccionalEdit'),
    url(r'^carrera_jurisdiccional$', 'apps.titulos.views.carrera_jurisdiccional.index', name='carreraJurisdiccional'),
    url(r'^carrera_jurisdiccional/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.carrera_jurisdiccional.revisar_jurisdiccion', name='carreraJurisdiccionalRevisarJurisdiccion'),
    # Cohorte Seguimiento
    url(r'^cohorte_seguimiento$', 'apps.titulos.views.cohorte_seguimiento.index', name='cohorteSeguimientoIndex'),
    url(r'^cohorte_seguimiento/cohorte_(?P<tipo_unidad_educativa>[a-z_]+)/(?P<cohorte_ue_id>[0-9]+)/confirmar$', 'apps.titulos.views.cohorte_seguimiento.confirmar', name='cohorteConfirmar'),
    #
    url(r'^cohorte_seguimiento/([0-9]+)/establecimiento/$', 'apps.titulos.views.cohorte_seguimiento.cohortes_unidad_educativa', { 'tipo_unidad_educativa': 'establecimiento' }, name='cohortesEstablecimientoIndex'),
    url(r'^cohorte_seguimiento/([0-9]+)/cohorte_establecimiento/$', 'apps.titulos.views.cohorte_seguimiento.seguimiento', { 'tipo_unidad_educativa': 'establecimiento' }, name='cohortesEstablecimientoSeguimiento'),
     #
    url(r'^cohorte_seguimiento/([0-9]+)/anexo/$', 'apps.titulos.views.cohorte_seguimiento.cohortes_unidad_educativa', { 'tipo_unidad_educativa': 'anexo' }, name='cohortesAnexoIndex'),
    url(r'^cohorte_seguimiento/([0-9]+)/cohorte_anexo/$', 'apps.titulos.views.cohorte_seguimiento.seguimiento', { 'tipo_unidad_educativa': 'anexo' }, name='cohortesAnexoSeguimiento'),
    #
    url(r'^cohorte_seguimiento/([0-9]+)/extension_aulica/$', 'apps.titulos.views.cohorte_seguimiento.cohortes_unidad_educativa', { 'tipo_unidad_educativa': 'extension_aulica' }, name='cohortesExtensionAulicaIndex'),
    url(r'^cohorte_seguimiento/([0-9]+)/cohorte_extension_aulica/$', 'apps.titulos.views.cohorte_seguimiento.seguimiento', { 'tipo_unidad_educativa': 'extension_aulica' }, name='cohortesExtensionAulicaSeguimiento'),
    #url(r'^cohorte/create$', 'apps.titulos.views.cohorte.create', { 'carrera_jurisdiccional_id': None }, name='cohorteCreate'), # Ya no se utiliza, sino que se asigna una cohorte al título
    #
    url(r'^carrera_jurisdiccional/([0-9]+)/generar-cohorte$', 'apps.titulos.views.cohorte.create', name='cohorteCreate'),
    url(r'^cohorte/([0-9]+)/editar$', 'apps.titulos.views.cohorte.edit', name='cohorteEdit'),
    url(r'^carrera_jurisdiccional/([0-9]+)/generar-cohorte$', 'apps.titulos.views.cohorte.create', name='cohorteCreate'),
    url(r'^carrera_jurisdiccional/([0-9]+)/cohortes$', 'apps.titulos.views.cohorte.cohortes_por_carrera_jurisdiccional', name='cohortesPorCarreraJurisdiccional'),
    url(r'^cohorte/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte.eliminar', name='cohorteEliminar'),
    url(r'^cohorte/([0-9]+)/asignar-establecimientos$', 'apps.titulos.views.cohorte.asignar_establecimientos', name='cohorteAsignarEstablecimientos'),
    url(r'^cohorte/([0-9]+)/asignar-anexos$', 'apps.titulos.views.cohorte.asignar_anexos', name='cohorteAsignarAnexos'),
    url(r'^cohorte/([0-9]+)/asignar-extensiones-aulicas$', 'apps.titulos.views.cohorte.asignar_extensiones_aulicas', name='cohorteAsignarExtensionesAulicas'),
    url(r'^cohorte$', 'apps.titulos.views.cohorte.index', name='cohorte'),
    url(r'^cohorte/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.cohorte.revisar_jurisdiccion', name='cohorteRevisarJurisdiccion'),
    # Cohorte establecimiento
    #url(r'^cohorte-establecimiento/([0-9]+)/confirmar$', 'apps.titulos.views.cohorte_establecimiento.confirmar', name='cohorteEstablecimientoConfirmar'),
    #url(r'^cohorte-establecimiento$', 'apps.titulos.views.cohorte_establecimiento.index', name='cohorteEstablecimientoIndex'),
    #url(r'^cohorte-establecimiento/([0-9]+)/seguimiento$', 'apps.titulos.views.cohorte_establecimiento.seguimiento', name='cohorteEstablecimientoSeguimiento'),
    #url(r'^cohorte-establecimiento/([0-9]+)/editar-seguimiento$', 'apps.titulos.views.cohorte_establecimiento.edit_seguimiento', name='cohorteEstablecimientoSeguimientoCreate'),
    #url(r'^cohorte-establecimiento/([0-9]+)/crear-seguimiento$', 'apps.titulos.views.cohorte_establecimiento.create_seguimiento', name='cohorteEstablecimientoSeguimientoEdit'),
    #url(r'^cohorte-establecimiento/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte_establecimiento.eliminar', name='cohorteEstablecimientoSeguimientoEliminar'),
    # Cohorte anexo
    #url(r'^cohorte-anexo/([0-9]+)/confirmar$', 'apps.titulos.views.cohorte_anexo.confirmar', name='cohorteAnexoConfirmar'),
    #url(r'^cohorte-anexo$', 'apps.titulos.views.cohorte_anexo.index', name='cohorteAnexoIndex'),
    #url(r'^cohorte-anexo/([0-9]+)/seguimiento$', 'apps.titulos.views.cohorte_anexo.seguimiento', name='cohorteAnexoSeguimiento'),
    #url(r'^cohorte-anexo/([0-9]+)/editar-seguimiento$', 'apps.titulos.views.cohorte_anexo.edit_seguimiento', name='cohorteAnexoSeguimientoCreate'),
    #url(r'^cohorte-anexo/([0-9]+)/crear-seguimiento$', 'apps.titulos.views.cohorte_anexo.create_seguimiento', name='cohorteAnexoSeguimientoEdit'),
    #url(r'^cohorte-anexo/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte_anexo.eliminar', name='cohorteAnexoSeguimientoEliminar'),
    # AJAX
    url(r'^ajax/get_titulos_por_tipo/(?P<tipo_titulo_id>[0-9]+)', 'apps.titulos.views.ajax.get_titulos_por_tipo', name='ajaxGetTitulosPorTipo'),
    url(r'^ajax/get_rango_anios_cohorte/(?P<carrera_jurisdiccional_id>[0-9]+)', 'apps.titulos.views.ajax.get_rango_anios_cohorte', name='ajaxGetRangoAniosCohorte'),
    # Proyecto
    url(r'^postitulo/create$', 'apps.titulos.views.postitulo.create', name='postituloCreate'),
    url(r'^postitulo/([0-9]+)/editar$', 'apps.titulos.views.postitulo.edit', name='postituloEdit'),
    url(r'^postitulo/([0-9]+)/delete$', 'apps.titulos.views.postitulo.delete', name='postituloDelete'),
    url(r'^postitulo$', 'apps.titulos.views.postitulo.index', name='postitulo'),
    # Carrera
    url(r'^carrera/create$', 'apps.titulos.views.carrera.create', name='carreraCreate'),
    url(r'^carrera/([0-9]+)/editar$', 'apps.titulos.views.carrera.edit', name='carreraEdit'),
    url(r'^carrera/([0-9]+)/delete$', 'apps.titulos.views.carrera.delete', name='carreraEliminar'),
    url(r'^carrera/([0-9]+)/titulos$', 'apps.titulos.views.carrera.titulos', name='carreraTitulos'),
    url(r'^carrera$', 'apps.titulos.views.carrera.index', name='carrera'),
    
)
