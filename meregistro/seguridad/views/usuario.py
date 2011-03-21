# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from seguridad.decorators import login_required
from seguridad.models import Usuario
from seguridad.forms import UsuarioFormFilters, UsuarioForm

@login_required
def index(request):
  """
  Búsqueda de usuarios
  """
  if request.method == 'POST':
    form_filter = UsuarioFormFilters(request.POST)
#    if form_filter.is_valid():
#      q = build_query(form_filter)
  else:
    form_filter = UsuarioFormFilters()
  q = build_query(form_filter, 1)
  return my_render(request, 'seguridad/usuario/index.html', {
    'form_filters': form_filter,
    'objects': q
  })

def build_query(filters, page):
  """
  Construye el query de búsqueda a partir de los filtros.
  """
  return filters.buildQuery().order_by('apellido', 'nombre')

@login_required
def edit(request, userId):
  if request.method == 'POST':
    form = UsuarioForm(request.POST, instance=Usuario.objects.get(pk=userId))
    if form.is_valid(): # guardar
      form.save()
  else:
    form = UsuarioForm(instance=Usuario.objects.get(pk=userId))

  return my_render(request, 'seguridad/usuario/edit.html', {
    'form': form
  })
