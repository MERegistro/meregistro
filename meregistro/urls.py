from django.conf.urls.defaults import *
from django.conf import settings
import apps.seguridad.urls as seguridad_urls
import apps.registro.urls as registro_urls
import apps.titulos.urls as titulos_urls
import apps.reportes.urls as reportes_urls

urlpatterns = patterns('',
    url(r'^login', 'apps.seguridad.views.login', name='login'),
    url(r'^logout', 'apps.seguridad.views.logout', name='logout'),
    url(r'^seguridad/', include(seguridad_urls)),
    url(r'^registro/', include(registro_urls)),
    url(r'^titulos/', include(titulos_urls)),
    url(r'^reportes/', include(reportes_urls)),
    url(r'^seleccionarPerfil', 'apps.seguridad.views.seleccionar_perfil', name='seleccionarPerfil'),
    url(r'^' + settings.STATIC_URL_PATH + '/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^$', 'apps.registro.views.index', name="index"),
)
