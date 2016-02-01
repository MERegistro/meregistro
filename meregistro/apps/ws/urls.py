# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns=patterns('',
    # Carrera
    url(r'^getOferta/anio/([0-9]+)$', 'apps.ws.views.getOfertaPorAnio', name='wsGetOfertaPorAnio'),
    url(r'^getPadronDepartamentos$', 'apps.ws.views.getPadronDepartamentos', name='wsGetDepartamentos'),
    url(r'^getDepartamentos/jurisdiccion/([0-9]+)$', 'apps.ws.views.getDepartamentosPorJurisdiccion', name='wsGetDepartamentosPorJurisdiccion'),
    url(r'^getPadronLocalidades$', 'apps.ws.views.getPadronLocalidades', name='wsGetLocalidades'),
    url(r'^getLocalidades/departamento/([0-9]+)$', 'apps.ws.views.getLocalidadesPorDepartamento', name='wsGetLocalidadesPorDepartamento'),
    url(r'^getPadronInstitutos$', 'apps.ws.views.getPadronInstitutos', name='wsGetPadronInstitutos'),
    url(r'^getInstitutos/localidad/([0-9]+)$', 'apps.ws.views.getInstitutosPorLocalidad', name='wsGetInstitutosPorLocalidad'),
    url(r'^getInstitutosEstatales/localidad/([0-9]+)$', 'apps.ws.views.getInstitutosEstatalesPorLocalidad', name='wsGetInstitutosEstatalesPorLocalidad'),
    url(r'^getPadronCarreras$', 'apps.ws.views.getPadronCarreras', name='wsGetPadronCarreras'),
    url(r'^getCarrerasPorInstituto/cueanexo/([0-9]+)/anio/([0-9]+)$', 'apps.ws.views.getCarrerasPorInstituto', name='wsGetCarrerasPorInstituto'),
)
