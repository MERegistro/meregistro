# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required

def index(request):
    if request.user.is_authenticated():
        extend_template = 'base_registro.html'
        template = 'registro/index/index.html'
    else:
        extend_template = 'base.html'
        template = 'registro/index/index_no_autenticado.html'
    return my_render(request, template, {
        'extend_template': extend_template
    })
