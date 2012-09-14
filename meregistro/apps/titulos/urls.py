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
    url(r'^normativa_jurisdiccional/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.normativa_jurisdiccional.revisar_jurisdiccion', name = 'normativaJurisdiccionalRevisarJurisdiccion'),
    # Normativa nacional
    url(r'^normativa_nacional/create$', 'apps.titulos.views.normativa_nacional.create', name = 'normativaNacionalCreate'),
    url(r'^normativa_nacional/([0-9]+)/editar$', 'apps.titulos.views.normativa_nacional.edit', name = 'normativaNacionalEdit'),
    url(r'^normativa_nacional/([0-9]+)/eliminar$', 'apps.titulos.views.normativa_nacional.delete', name = 'normativaNacionalEliminar'),
    url(r'^normativa_nacional$', 'apps.titulos.views.normativa_nacional.index', name = 'normativaNacional'),
    # Matriculas
    url(r'^matricula/create$', 'apps.titulos.views.matricula.create', name = 'matriculaCreate'),
    url(r'^matricula/([0-9]+)/editar$', 'apps.titulos.views.matricula.edit', name = 'matriculaEdit'),
    url(r'^matricula/([0-9]+)/delete$', 'apps.titulos.views.matricula.delete', name = 'matriculaDelete'),
    url(r'^matricula$', 'apps.titulos.views.matricula.index', name = 'matricula'),
    url(r'^matricula/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.matricula.revisar_jurisdiccion', name = 'matriculaRevisarJurisdiccion'),
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
    url(r'^titulo_jurisdiccional/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.titulo_jurisdiccional.revisar_jurisdiccion', name = 'tituloJurisdiccionalRevisarJurisdiccion'),
    # Cohorte
    #url(r'^cohorte/create$', 'apps.titulos.views.cohorte.create', { 'titulo_jurisdiccional_id': None }, name = 'cohorteCreate'), # Ya no se utiliza, sino que se asigna una cohorte al título
    url(r'^cohorte/([0-9]+)/editar$', 'apps.titulos.views.cohorte.edit', name = 'cohorteEdit'),
    url(r'^titulo_jurisdiccional/([0-9]+)/asignar-cohorte$', 'apps.titulos.views.cohorte.create', name = 'cohorteCreate'),
    url(r'^titulo_jurisdiccional/([0-9]+)/cohortes$', 'apps.titulos.views.cohorte.cohortes_por_titulo', name = 'cohortesPorTitulo'),
    url(r'^cohorte/([0-9]+)/eliminar$', 'apps.titulos.views.cohorte.eliminar', name = 'cohorteEliminar'),
    url(r'^cohorte/([0-9]+)/asignar-establecimientos$', 'apps.titulos.views.cohorte.asignar_establecimientos', name = 'cohorteAsignarEstablecimientos'),
    url(r'^cohorte/([0-9]+)/asignar-anexos$', 'apps.titulos.views.cohorte.asignar_anexos', name = 'cohorteAsignarAnexos'),
    url(r'^cohorte/([0-9]+)/asignar-extensiones-aulicas$', 'apps.titulos.views.cohorte.asignar_extensiones_aulicas', name = 'cohorteAsignarExtensionesAulicas'),
    url(r'^cohorte$', 'apps.titulos.views.cohorte.index', name = 'cohorte'),
    url(r'^cohorte/([0-9]+)/revisar_jurisdiccion$', 'apps.titulos.views.cohorte.revisar_jurisdiccion', name = 'cohorteRevisarJurisdiccion'),
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
    # Egresados establecimiento
    url(r'^establecimiento/titulo/([0-9]+)/agregar-egresados$', 'apps.titulos.views.egresados_establecimiento.create', name = 'establecimientoEgresadosCreate'),
    url(r'^establecimiento/egresados-por-titulo/([0-9]+)/editar$', 'apps.titulos.views.egresados_establecimiento.edit', name = 'establecimientoEgresadosEdit'),
    url(r'^establecimiento/egresados-por-titulo/([0-9]+)/detalle$', 'apps.titulos.views.egresados_establecimiento.detalle', name = 'establecimientoEgresadosDetalle'),
    url(r'^establecimiento/egresados/([0-9]+)/agregar-detalle$', 'apps.titulos.views.egresados_establecimiento.agregar_detalle', name = 'establecimientoEgresadosAgregarDetalle'),
    url(r'^establecimiento/egresados/([0-9]+)/editar-detalle$', 'apps.titulos.views.egresados_establecimiento.edit_detalle', name = 'establecimientoEgresadosEditDetalle'),
    url(r'^establecimiento/titulo/([0-9]+)/egresados$', 'apps.titulos.views.egresados_establecimiento.egresados_por_titulo', name = 'establecimientoEgresadosPorTitulo'),
    url(r'^establecimiento/egresados$', 'apps.titulos.views.egresados_establecimiento.index', name = 'establecimientoEgresados'),
    url(r'^establecimiento/egresados/([0-9]+)/eliminar$', 'apps.titulos.views.egresados_establecimiento.eliminar', name = 'establecimientoEgresadosEliminar'),
    url(r'^establecimiento/egresados/([0-9]+)/eliminar_detalle$', 'apps.titulos.views.egresados_establecimiento.eliminar_detalle', name = 'establecimientoEgresadosDetalleEliminar'),
    # Egresados anexo
    url(r'^anexo/titulo/([0-9]+)/agregar-egresados$', 'apps.titulos.views.egresados_anexo.create', name = 'anexoEgresadosCreate'),
    url(r'^anexo/egresados-por-titulo/([0-9]+)/editar$', 'apps.titulos.views.egresados_anexo.edit', name = 'anexoEgresadosEdit'),
    url(r'^anexo/egresados-por-titulo/([0-9]+)/detalle$', 'apps.titulos.views.egresados_anexo.detalle', name = 'anexoEgresadosDetalle'),
    url(r'^anexo/egresados/([0-9]+)/agregar-detalle$', 'apps.titulos.views.egresados_anexo.agregar_detalle', name = 'anexoEgresadosAgregarDetalle'),
    url(r'^anexo/egresados/([0-9]+)/editar-detalle$', 'apps.titulos.views.egresados_anexo.edit_detalle', name = 'anexoEgresadosEditDetalle'),
    url(r'^anexo/titulo/([0-9]+)/egresados$', 'apps.titulos.views.egresados_anexo.egresados_por_titulo', name = 'anexoEgresadosPorTitulo'),
    url(r'^anexo/egresados$', 'apps.titulos.views.egresados_anexo.index', name = 'anexoEgresados'),
    url(r'^anexo/egresados/([0-9]+)/eliminar$', 'apps.titulos.views.egresados_anexo.eliminar', name = 'anexoEgresadosEliminar'),
    url(r'^anexo/egresados/([0-9]+)/eliminar_detalle$', 'apps.titulos.views.egresados_anexo.eliminar_detalle', name = 'anexoEgresadosDetalleEliminar'),
    # Carrera
    url(r'^carrera/create$', 'apps.titulos.views.carrera.create', name = 'carreraCreate'),
    url(r'^carrera/([0-9]+)/editar$', 'apps.titulos.views.carrera.edit', name = 'carreraEdit'),
    url(r'^carrera/([0-9]+)/delete$', 'apps.titulos.views.carrera.delete', name = 'carreraEliminar'),
    url(r'^carrera$', 'apps.titulos.views.carrera.index', name = 'carrera'),
    
)
