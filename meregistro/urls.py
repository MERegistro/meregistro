from django.conf.urls.defaults import *
from django.conf import settings
import apps.seguridad.urls as seguridad_urls
import apps.registro.urls as registro_urls
import apps.titulos.urls as titulos_urls
import apps.reportes.urls as reportes_urls
import apps.sistema.urls as sistema_urls
import apps.backend.urls as backend_urls
import apps.consulta_validez.urls as consulta_validez_urls
import apps.oferta_nacional.urls as oferta_nacional_urls
import apps.validez_nacional.urls as validez_nacional_urls
import apps.postitulos.urls as postitulos_urls

urlpatterns = patterns('',
    url(r'^login', 'apps.seguridad.views.login', name='login'),
    url(r'^logout', 'apps.seguridad.views.logout', name='logout'),
    url(r'^remember_password', 'apps.seguridad.views.remember_password', name='remember_password'),
    url(r'^reset_password/([1234567890qwertyuiopasdfghjklzxcvbnm]+)', 'apps.seguridad.views.reset_password', name='reset_password'),
    url(r'^seguridad/', include(seguridad_urls)),
    url(r'^registro/', include(registro_urls)),
    url(r'^titulos/', include(titulos_urls)),
    url(r'^postitulos/', include(postitulos_urls)),
    url(r'^reportes/', include(reportes_urls)),
    url(r'^sistema/', include(sistema_urls)),
    url(r'^backend/', include(backend_urls)),
    url(r'^consulta_validez/', include(consulta_validez_urls)),
    url(r'^oferta_nacional/', include(oferta_nacional_urls)),
    url(r'^validez_nacional/', include(validez_nacional_urls)),
    url(r'^seleccionarPerfil', 'apps.seguridad.views.seleccionar_perfil', name='seleccionarPerfil'),
    url(r'^' + settings.STATIC_URL_PATH + '/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),
    url(r'^$', 'apps.registro.views.index', name="index"),
)
