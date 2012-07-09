# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from django.core.paginator import Paginator

class CrudConfig:
  def __init__(self, model_class, form_class, form_filter_class, template_dir):
    self.model_class = model_class
    self.form_class = form_class
    self.form_filter_class = form_filter_class
    self.template_dir = template_dir

from apps.registro.models import AutoridadCargo
from apps.registro.forms import AutoridadCargoForm, AutoridadCargoFormFilters

cruds = {
  'autoridad_cargo': CrudConfig(AutoridadCargo, AutoridadCargoForm, AutoridadCargoFormFilters, 'backend/autoridad_cargo/')
}
ITEMS_PER_PAGE = 50


@credential_required('seg_backend')
def index(request, crud_name):
  config = cruds[crud_name]
  if request.method == 'GET':
    form_filter = config.form_filter_class(request.GET)
  else:
    form_filter = config.form_filter_class()
  q = build_query(form_filter, 1)
  paginator = Paginator(q, ITEMS_PER_PAGE)

  try:
    page_number = int(request.GET['page'])
  except (KeyError, ValueError):
    page_number = 1
  if page_number < 1:
    page_number = 1
  elif page_number > paginator.num_pages:
    page_number = paginator.num_pages

  page = paginator.page(page_number)
  objects = page.object_list

  return my_render(request, config.template_dir + 'index.html', {
      'form_filters': form_filter,
      'objects': objects,
      'paginator': paginator,
      'page': page,
      'page_number': page_number,
      'pages_range': range(1, paginator.num_pages + 1),
      'next_page': page_number + 1,
      'prev_page': page_number - 1
  })


def build_query(filters, page):
  """
  Construye el query de búsqueda a partir de los filtros.
  """
  return filters.buildQuery()


@credential_required('seg_backend')
def create(request, crud_name):
  config = cruds[crud_name]
  if request.method == 'POST':
    form = config.form_class(request.POST)
    if form.is_valid():
      obj = form.save()
      request.set_flash('success', 'Datos guardados correctamente.')
      # redirigir a edit
      return HttpResponseRedirect(reverse('crudEdit', args=[crud_name, obj.id]))
    else:
      request.set_flash('warning', 'Ocurrió un error guardando los datos.')
  else:
    form = config.form_class()

  return my_render(request, config.template_dir + 'new.html', {
    'form': form,
    'is_new': True,
  })


@credential_required('seg_backend')
def edit(request, crud_name, obj_id):
  config = cruds[crud_name]
  obj = config.model_class.objects.get(pk=obj_id)
  if request.method == 'POST':
    form = config.form_class(request.POST, instance=obj)
    if form.is_valid():
      obj = form.save()
      request.set_flash('success', 'Datos actualizados correctamente.')
    else:
      request.set_flash('warning', 'Ocurrió un error actualizando los datos.')
  else:
      form = config.form_class(instance=obj)
  return my_render(request, config.template_dir + 'edit.html', {
    'form': form,
    'obj': obj,
  })


@credential_required('seg_backend')
def delete(request, crud_name, obj_id):
  config = cruds[crud_name]
  obj = config.model_class.objects.get(pk=obj_id)
  try:
    obj.delete()
    request.set_flash('success', 'Registro eliminado correctamente.')
  except:
    request.set_flash('warning', 'No se puede eliminar el elemento porque está en uso.')
  return HttpResponseRedirect(reverse('crudList', args=[crud_name]))
