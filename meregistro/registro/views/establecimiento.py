# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from datetime import datetime
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from seguridad.decorators import login_required
from seguridad.models import Usuario, Perfil
from registro.models import Establecimiento, Estado
from registro.forms import EstablecimientoFormFilters, EstablecimientoForm


@login_required
def index(request):
  """
  Búsqueda de establecimientos
  """
  if request.method == 'POST':
    form_filter = EstablecimientoFormFilters(request.POST)
#    if form_filter.is_valid():
#      q = build_query(form_filter)
  else:
    form_filter = EstablecimientoFormFilters()
  q = build_query(form_filter, 1)
  return my_render(request, 'registro/establecimiento/index.html', {
    'form_filters': form_filter,
    'objects': q
  })

def build_query(filters, page):
  """
  Construye el query de búsqueda a partir de los filtros.
  """
  return filters.buildQuery().order_by('nombre')

@login_required
def create(request):
  """
  Alta de establecimiento.
  """
  if request.method == 'POST':
    form = EstablecimientoForm(request.POST)
    if form.is_valid(): # guardar
      establecimiento = form.save(commit = False)
      establecimiento.estado = Estado.objects.get(nombre = 'Pendiente')
      establecimiento.save()

      request.set_flash('success', 'Datos guardados correctamente.')

      # redirigir a edit
      return HttpResponseRedirect(reverse('establecimientoEdit', args=[establecimiento.id]))
    else:
      request.set_flash('warning', 'Ocurrió un error guardando los datos.')
  else:
    form = EstablecimientoForm()

  return my_render(request, 'registro/establecimiento/new.html', {
    'form': form,
  })

@login_required
def edit(request, establecimiento_id):
  """
  Edición de los datos de un establecimiento.
  """
  establecimiento = Establecimiento.objects.get(pk = establecimiento_id)
  if request.method == 'POST':
    form = EstablecimientoForm(request.POST, instance = establecimiento)
    if form.is_valid(): # guardar
      establecimiento = form.save()
      request.set_flash('success', 'Datos actualizados correctamente.')
    else:
      request.set_flash('warning','Ocurrió un error actualizando los datos.')
  else:
    form = EstablecimientoForm(instance = establecimiento)

  return my_render(request, 'registro/establecimiento/edit.html', {
    'form': form,
    'establecimiento': establecimiento,
  })
