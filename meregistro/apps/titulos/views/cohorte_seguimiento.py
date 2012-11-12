# -*- coding: UTF-8 -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from meregistro.shortcuts import my_render
from apps.seguridad.decorators import login_required, credential_required
from apps.seguridad.models import TipoAmbito
from apps.titulos.models import CohorteEstablecimiento, CohorteAnexo, CohorteExtensionAulica, EstadoCarreraJurisdiccional
from apps.titulos.forms import CohortesUnidadEducativaFormFilters
from apps.registro.models import Jurisdiccion, Establecimiento, Anexo, ExtensionAulica
from django.core.paginator import Paginator
from helpers.MailHelper import MailHelper
import datetime

ITEMS_PER_PAGE = 50


@login_required	
def __get_ue_actual(request, tipo):
	"""
	Trae la unidad educativa del usuario
	"""
	if tipo.nombre == TipoAmbito.TIPO_SEDE:
		return Establecimiento.objects.get(ambito__id=request.get_perfil().ambito.id)
	elif tipo.nombre == TipoAmbito.TIPO_ANEXO:
		return Anexo.objects.get(ambito__id=request.get_perfil().ambito.id)
	elif tipo.nombre == TipoAmbito.TIPO_EXTENSION_AULICA:
		return ExtensionAulica.objects.get(ambito__id=request.get_perfil().ambito.id)
	else:
		raise Exception('ERROR: El usuario no tiene asignado una unidad educativa.')

"""
Pantalla en la cual se listan las unidades educativas del usuario
"""
@login_required
@credential_required('tit_cohorte_seguimiento')
def index(request):
	tipo_perfil = request.get_perfil().ambito.tipo
	
	unidad_educativa = __get_ue_actual(request, tipo_perfil)
	
	if unidad_educativa.__class__ == Establecimiento:
		establecimiento = unidad_educativa
	elif unidad_educativa.__class__ == Anexo or unidad_educativa.__class__ == ExtensionAulica:
		establecimiento = unidad_educativa.establecimiento
	
	anexos = establecimiento.anexos
	extensiones_aulicas = establecimiento.extensiones_aulicas

	return my_render(request, 'titulos/cohorte/cohorte_seguimiento/index.html', {
		'establecimiento': establecimiento,
		'anexos': anexos.all(),
		'extensiones_aulicas': extensiones_aulicas.all(),
		'unidad_educativa_actual': unidad_educativa,
		'tipo_perfil': tipo_perfil.nombre
	})


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def cohortes_unidad_educativa(request, unidad_educativa_id, tipo_unidad_educativa):
	"""
	Index de cohorte unidad educativa
	"""
	if tipo_unidad_educativa == 'establecimiento':
		unidad_educativa = Establecimiento.objects.get(pk=unidad_educativa_id, ambito__path__istartswith=request.get_perfil().ambito.path)
		titulo_interfaz = 'Seguimiento de Cohorte de la Sede'
	elif tipo_unidad_educativa == 'anexo':
		unidad_educativa = Anexo.objects.get(pk=unidad_educativa_id, ambito__path__istartswith=request.get_perfil().ambito.path)
		titulo_interfaz = 'Seguimiento de Cohorte del Anexo'
	elif tipo_unidad_educativa == 'extension_aulica':
		unidad_educativa = ExtensionAulica.objects.get(pk=unidad_educativa_id, ambito__path__istartswith=request.get_perfil().ambito.path)
		titulo_interfaz = 'Seguimiento de Cohorte de la Extensión Áulica'
		
	form_filter = CohortesUnidadEducativaFormFilters(request.GET, tipo_unidad_educativa=tipo_unidad_educativa)
		
	q = build_confirmar_cohortes_query(form_filter, 1, request, tipo_unidad_educativa, unidad_educativa_id)

	paginator = Paginator(q, ITEMS_PER_PAGE)

	try:
		page_number = int(request.GET['page'])
	except (KeyError, ValueError):
		page_number = 1
	# chequear los límites
	if page_number < 1:
		page_number = 1
	elif page_number > paginator.num_pages:
		page_number = paginator.num_pages

	page = paginator.page(page_number)
	objects = page.object_list
	return my_render(request, 'titulos/cohorte/cohorte_seguimiento/cohortes_unidad_educativa.html', {
		'form_filters': form_filter,
		'objects': objects,
		'tipo_unidad_educativa': tipo_unidad_educativa,
		'unidad_educativa': unidad_educativa,
		'titulo_interfaz': titulo_interfaz,
		'paginator': paginator,
		'page': page,
		'page_number': page_number,
		'pages_range': range(1, paginator.num_pages + 1),
		'next_page': page_number + 1,
		'prev_page': page_number - 1
	})



def build_confirmar_cohortes_query(filters, page, request, tipo_unidad_educativa, unidad_educativa_id):
	"""
	Construye el query de búsqueda a partir de los filtros.
	"""
	estado = EstadoCarreraJurisdiccional.objects.get(nombre=EstadoCarreraJurisdiccional.CONTROLADO)
	# Filtra que el año de la última cohorte sea menor o igual al año en curso y el estado sea controlado
	if tipo_unidad_educativa == 'establecimiento':
		filters.buildQuery().filter(establecimiento__id=unidad_educativa_id)
	elif tipo_unidad_educativa == 'anexo':
		filters.buildQuery().filter(anexo__id=unidad_educativa_id)
	elif tipo_unidad_educativa == 'extension_alica':
		filters.buildQuery().filter(extension_aulica__id=unidad_educativa_id)
	return filters.buildQuery()
	return filters.buildQuery().filter(cohorte__carrera_jurisdiccional__estado__nombre=estado).order_by('cohorte__carrera_jurisdiccional__titulo__nombre', '-cohorte__anio')




@login_required
#@credential_required('tit_cohorte_seguimiento')
def seguimiento(request, cohorte_ue_id, tipo_ue):
	"""
	Seguimiento de cohorte de la unidad educativa
	"""
	if tipo_ue == 'Establecimiento':
		objects = CohorteEstablecimientoSeguimiento.objects.filter(cohorte_establecimiento__id=cohorte_ue_id).order_by('anio')
	elif tipo_ue == 'Anexo':
		objects = CohorteAnexoSeguimiento.objects.filter(cohorte_anexo__id=cohorte_ue_id).order_by('anio')
	elif tipo_ue == 'ExtensionAulica':
		objects = CohorteExtensionAulicaSeguimiento.objects.filter(cohorte_extension_aulica__id=cohorte_ue_id).order_by('anio')
	
	#establecimiento = __get_establecimiento_actual(request)
	cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk=cohorte_establecimiento_id)

	if cohorte_establecimiento.inscriptos is None:  # No aceptada
		request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
		return HttpResponseRedirect(reverse('cohorteEstablecimientoIndex'))

	objects = CohorteEstablecimientoSeguimiento.objects.filter(cohorte_establecimiento=cohorte_establecimiento).order_by('anio')
	return my_render(request, 'titulos/cohorte/cohorte_seguimiento/seguimiento.html', {
		'objects': objects,
		'cohorte_establecimiento': cohorte_establecimiento,
		'page_title': 'Seguimiento de cohote',
		'current_page': 'seguimiento',
	})


@login_required
#@credential_required('tit_cohorte_aceptar_asignacion')
def confirmar(request, cohorte_establecimiento_id):
	"""
	Confirmar cohorte
	"""
	cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk=cohorte_establecimiento_id)

	if request.method == 'POST':
		form = CohorteEstablecimientoConfirmarForm(request.POST, instance=cohorte_establecimiento)
		if form.is_valid():
			cohorte_establecimiento = form.save(commit=False)
			estado = EstadoCohorteEstablecimiento.objects.get(nombre=EstadoCohorteEstablecimiento.ACEPTADA)
			cohorte_establecimiento.estado = estado
			cohorte_establecimiento.save()
			cohorte_establecimiento.registrar_estado()

			request.set_flash('success', 'La cohorte fue confirmada correctamente.')
			""" Redirecciono para evitar el reenvío del form """
			return HttpResponseRedirect(reverse('cohorteEstablecimientoIndex'))

		else:
			request.set_flash('warning', 'Ocurrió un error confirmando la cohorte.')
	else:
		form = CohorteEstablecimientoConfirmarForm(instance=cohorte_establecimiento)

	return my_render(request, 'titulos/cohorte/cohorte_establecimiento/confirmar.html', {
		'cohorte_establecimiento': cohorte_establecimiento,
		'cohorte': cohorte_establecimiento.cohorte,
		'form': form,
	})




@login_required
#@credential_required('tit_cohorte_seguimiento')
def create_seguimiento(request, cohorte_establecimiento_id):

	cohorte_establecimiento = CohorteEstablecimiento.objects.get(pk=cohorte_establecimiento_id)
	if cohorte_establecimiento.inscriptos is None:  # No aceptada
		request.set_flash('warning', 'No se puede generar años de seguimiento a cohortes no aceptadas.')
		return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args=[cohorte_establecimiento.id]))

	if request.method == 'POST':
		form = CohorteEstablecimientoSeguimientoForm(request.POST, inscriptos_total=cohorte_establecimiento.inscriptos, anio_cohorte=cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id=cohorte_establecimiento.id)
		if form.is_valid():
			seguimiento = form.save(commit=False)
			seguimiento.cohorte_establecimiento = cohorte_establecimiento
			seguimiento.save()

			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args=[cohorte_establecimiento.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CohorteEstablecimientoSeguimientoForm(inscriptos_total=cohorte_establecimiento.inscriptos, anio_cohorte=cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id=cohorte_establecimiento.id)

	return my_render(request, 'titulos/cohorte/cohorte_establecimiento/new.html', {
		'form': form,
		'cohorte_establecimiento': cohorte_establecimiento,
		'form_template': 'titulos/cohorte/cohorte_establecimiento/form_seguimiento.html',
		'page_title': 'Datos de seguimiento',
		'current_page': 'datos_seguimiento',
	})


@login_required
#@credential_required('tit_cohorte_seguimiento')
def edit_seguimiento(request, seguimiento_id):
	"""
	Confirmar cohorte
	"""
	seguimiento = CohorteEstablecimientoSeguimiento.objects.get(pk=seguimiento_id)
	cohorte_establecimiento = seguimiento.cohorte_establecimiento

	if request.method == 'POST':
		form = CohorteEstablecimientoSeguimientoForm(request.POST, instance=seguimiento, inscriptos_total=cohorte_establecimiento.inscriptos, anio_cohorte=cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id=cohorte_establecimiento.id)
		if form.is_valid():
			seguimiento = form.save(commit=False)
			seguimiento.cohorte_establecimiento = cohorte_establecimiento
			seguimiento.save()

			request.set_flash('success', 'Datos guardados correctamente.')
			# redirigir a edit
			return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args=[cohorte_establecimiento.id]))
		else:
			request.set_flash('warning', 'Ocurrió un error guardando los datos.')
	else:
		form = CohorteEstablecimientoSeguimientoForm(instance=seguimiento, inscriptos_total=cohorte_establecimiento.inscriptos, anio_cohorte=cohorte_establecimiento.cohorte.anio, cohorte_establecimiento_id=cohorte_establecimiento.id)

	return my_render(request, 'titulos/cohorte/cohorte_establecimiento/edit.html', {
		'form': form,
		'cohorte_establecimiento': cohorte_establecimiento,
		'form_template': 'titulos/cohorte/cohorte_establecimiento/form_seguimiento.html',
		'page_title': 'Datos de seguimiento',
		'current_page': 'datos_seguimiento',
	})


@login_required
#@credential_required('tit_cohorte_seguimiento')
def eliminar(request, seguimiento_id):
	"""
	Eliminación de año de seguimiento de cohorte
	"""
	seguimiento = CohorteEstablecimientoSeguimiento.objects.get(pk=seguimiento_id)

	if request.method == 'POST':
		if int(request.POST['seguimiento_id']) is not int(seguimiento.id):
			raise Exception('Error en la consulta!')

		seguimiento.delete()
		request.set_flash('success', 'El año de seguimiento fue eliminado correctamente.')
		""" Redirecciono para evitar el reenvío del form """
		return HttpResponseRedirect(reverse('cohorteEstablecimientoSeguimiento', args=[seguimiento.cohorte_establecimiento.id]))
	else:
		request.set_flash('warning', 'Está seguro de eliminar el año de seguimiento? Esta operación no puede deshacerse.')
	return my_render(request, 'titulos/cohorte/cohorte_establecimiento/eliminar.html', {
		'seguimiento_id': seguimiento.id,
	})
