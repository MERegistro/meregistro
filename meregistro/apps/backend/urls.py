# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'apps.backend.views.index', name='backendHome'),
    url(r'^solapas_establecimiento$', 'apps.backend.views.configurar_solapas_establecimiento', name='backendSolapasEstablecimiento'),
    url(r'^solapas_anexo$', 'apps.backend.views.configurar_solapas_anexo', name='backendSolapasAnexo'),
    url(r'^solapas_extension_aulica$', 'apps.backend.views.configurar_solapas_extension_aulica', name='backendSolapasExtensionAulica'),
    url(r'^crud/(.*)/$', 'apps.backend.views.crud.index', name='crudList'),
    url(r'^crud/(.*)/([0-9]+)/edit', 'apps.backend.views.crud.edit', name='crudEdit'),
    url(r'^crud/(.*)/create', 'apps.backend.views.crud.create', name='crudCreate'),
    url(r'^crud/(.*)/([0-9]+)/delete', 'apps.backend.views.crud.delete', name='crudDelete'),
  )
