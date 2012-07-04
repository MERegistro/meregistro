# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import Usuario, Perfil

@login_required
def ayuda(request):
    return my_render(request, 'sistema/pages/ayuda.html', {
    })
