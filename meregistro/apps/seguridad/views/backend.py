# -*- coding: UTF-8 -*-

from meregistro.shortcuts import my_render
from apps.seguridad.decorators import credential_required
from apps.seguridad.forms import ConfiguracionSolapasEstablecimientoForm
from apps.seguridad.models import ConfiguracionSolapasEstablecimiento
from apps.seguridad.forms import ConfiguracionSolapasAnexoForm
from apps.seguridad.models import ConfiguracionSolapasAnexo
from apps.seguridad.forms import ConfiguracionSolapasExtensionAulicaForm
from apps.seguridad.models import ConfiguracionSolapasExtensionAulica


@credential_required('seg_backend')
def index(request):
  return my_render(request, 'seguridad/backend/index.html')

@credential_required('seg_backend')
def configurar_solapas_establecimiento(request):
  solapas_config = ConfiguracionSolapasEstablecimiento.get_instance()
  if request.method == 'POST':
    form = ConfiguracionSolapasEstablecimientoForm(request.POST, instance=solapas_config)
    if form.is_valid():
      form.save()
      request.set_flash('success', 'Datos guardados correctamente.')
    else:
      request.set_flash('warning', 'Ocurrió un error guardando los datos.')
  else:
      form = ConfiguracionSolapasEstablecimientoForm(instance=solapas_config)
  
  return my_render(request, 'seguridad/backend/solapas_establecimiento.html', {
      'form': form,
  })


@credential_required('seg_backend')
def configurar_solapas_anexo(request):
  solapas_config = ConfiguracionSolapasAnexo.get_instance()
  if request.method == 'POST':
    form = ConfiguracionSolapasAnexoForm(request.POST, instance=solapas_config)
    if form.is_valid():
      form.save()
      request.set_flash('success', 'Datos guardados correctamente.')
    else:
      request.set_flash('warning', 'Ocurrió un error guardando los datos.')
  else:
      form = ConfiguracionSolapasAnexoForm(instance=solapas_config)
  
  return my_render(request, 'seguridad/backend/solapas_anexo.html', {
      'form': form,
  })


@credential_required('seg_backend')
def configurar_solapas_extension_aulica(request):
  solapas_config = ConfiguracionSolapasExtensionAulica.get_instance()
  if request.method == 'POST':
    form = ConfiguracionSolapasExtensionAulicaForm(request.POST, instance=solapas_config)
    if form.is_valid():
      form.save()
      request.set_flash('success', 'Datos guardados correctamente.')
    else:
      request.set_flash('warning', 'Ocurrió un error guardando los datos.')
  else:
      form = ConfiguracionSolapasExtensionAulicaForm(instance=solapas_config)
  
  return my_render(request, 'seguridad/backend/solapas_extension_aulica.html', {
      'form': form,
  })

