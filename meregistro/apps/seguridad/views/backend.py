# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from apps.seguridad.decorators import credential_required

@credential_required('seg_backend')
def index(request):
  return my_render(request, 'seguridad/backend/index.html')
