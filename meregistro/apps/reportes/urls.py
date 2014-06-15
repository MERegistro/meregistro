# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *
from apps.registro.models.Establecimiento import Establecimiento

urlpatterns = patterns('',
    url(r'^establecimientos$', 'apps.reportes.views.establecimiento.establecimientos', name='reporteEstablecimientos'),
    # Estadística
    url(r'^estadistica/datos-generales$', 'apps.reportes.views.estadistica.datos_generales', name='estadisticaDatosGenerales'),
    #
    url(r'^datos-basicos/sedes$', 'apps.reportes.views.datos_basicos.sedes', name='reporteDatosBasicosSedes'),
    url(r'^datos-basicos/anexos$', 'apps.reportes.views.datos_basicos.anexos', name='reporteDatosBasicosAnexos'),
    url(r'^datos-basicos/extensiones-aulicas$', 'apps.reportes.views.datos_basicos.extensiones_aulicas', name='reporteDatosBasicosExtensionesAulicas'),
)
