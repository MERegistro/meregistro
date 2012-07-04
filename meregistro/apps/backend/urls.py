# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.backend.views.index', name='backendHome'),
    url(r'^solapas_establecimiento$', 'apps.backend.views.configurar_solapas_establecimiento', name='backendSolapasEstablecimiento'),
    url(r'^solapas_anexo$', 'apps.backend.views.configurar_solapas_anexo', name='backendSolapasAnexo'),
    url(r'^solapas_extension_aulica$', 'apps.backend.views.configurar_solapas_extension_aulica', name='backendSolapasExtensionAulica'),
  )
