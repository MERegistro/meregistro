# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required

ITEMS_PER_PAGE = 50

@login_required
def index(request):
    """
    Búsqueda de titulos
    """
    return my_render(request, 'titulos/titulo/index.html', {

    })
