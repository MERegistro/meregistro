# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from seguridad.decorators import login_required

@login_required
def index(request):
  """
  Pantalla de inicio. Portada del sistema.
  """
  return my_render(request, 'index.html')
