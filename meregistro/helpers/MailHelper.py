# -*- coding: utf-8 -*-
from django.db import models
from apps.seguridad.models import Usuario, Rol
from django.core.mail import send_mail, EmailMultiAlternatives
from settings import DEBUG, PROJECT_ROOT
from apps.seguridad.middleware import get_current_user
import datetime

class MailHelper():
    """
    Wrapper para envío de emails del sistema
    """
    EMAIL_FROM_DEFAULT = u'admin@example.com'

    ESTABLECIMIENTO_CREATE = u'EstablecimientoCreate'
    ESTABLECIMIENTO_UPDATE = u'EstablecimientoUpdate'
    ESTABLECIMIENTO_DELETE = u'EstablecimientoDelete'

    ANEXO_CREATE = u'AnexoCreate'
    ANEXO_UPDATE = u'AnexoUpdate'
    ANEXO_DELETE = u'AnexoDelete'

    EXTENSION_AULICA_CREATE = u'ExtensionAulicaCreate'
    EXTENSION_AULICA_UPDATE = u'ExtensionAulicaUpdate'
    EXTENSION_AULICA_DELETE = u'ExtensionAulicaDelete'

    TITULO_CREATE = u'TituloCreate'
    TITULO_UPDATE = u'TituloUpdate'
    TITULO_DELETE = u'TituloDelete'
    
    CERTIFICACION_CARGA_ESTABLECIMIENTO = u'CertificacionCargaEstablecimiento'
    CERTIFICACION_CARGA_ANEXO = u'CertificacionCargaAnexo'
    CERTIFICACION_CARGA_EXTENSION_AULICA = u'CertificacionCargaExtensionAulica'

    NUMERACION_SOLICITUD = u'NumeracionSolicitud'
    
    debug_count = 0

    @staticmethod
    def get_usuarios_activos_por_rol(rol):
        return Usuario.objects.filter(perfiles__rol__nombre=rol, perfiles__fecha_desasignacion=None, is_active=True)


    @staticmethod
    def notify_by_email(notification_type = None, model = None):
        """
        Funcionalidad básica de notificación
        """
        """ Diccionario con la llamada correspondiente al tipo de notificación que llega """
        mail_data_call_dict = {
            MailHelper.ESTABLECIMIENTO_CREATE: MailHelper.establecimiento_create,
            MailHelper.ESTABLECIMIENTO_UPDATE: MailHelper.establecimiento_update,
            MailHelper.ESTABLECIMIENTO_DELETE: MailHelper.establecimiento_delete,
            MailHelper.ANEXO_CREATE: MailHelper.anexo_create,
            MailHelper.ANEXO_UPDATE: MailHelper.anexo_update,
            MailHelper.ANEXO_DELETE: MailHelper.anexo_delete,
            MailHelper.EXTENSION_AULICA_CREATE: MailHelper.extension_aulica_create,
            MailHelper.EXTENSION_AULICA_UPDATE: MailHelper.extension_aulica_update,
            MailHelper.EXTENSION_AULICA_DELETE: MailHelper.extension_aulica_delete,
            MailHelper.TITULO_CREATE: MailHelper.titulo_create,
            MailHelper.TITULO_UPDATE: MailHelper.titulo_update,
            MailHelper.TITULO_DELETE: MailHelper.titulo_delete,
            MailHelper.CERTIFICACION_CARGA_ESTABLECIMIENTO: MailHelper.certificacion_carga_establecimiento,
            MailHelper.CERTIFICACION_CARGA_ANEXO: MailHelper.certificacion_carga_anexo,
            MailHelper.CERTIFICACION_CARGA_EXTENSION_AULICA: MailHelper.certificacion_carga_extension_aulica,
            MailHelper.NUMERACION_SOLICITUD: MailHelper.numeracion_solicitud,

        }
        """ EJ:  mail_data = MailHelper.establecimiento_create(model) """
        mail_data = mail_data_call_dict[notification_type](model)

        try:
            email_from = mail_data['email_from']
        except KeyError:
            email_from = MailHelper.EMAIL_FROM_DEFAULT

        if DEBUG:
            MailHelper.debug_email(model, mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], notification_type)
        else:
            msg = EmailMultiAlternatives(mail_data['subject'],
              mail_data['message'],
              email_from, mail_data['recipients'])
            if 'html' in mail_data:
              msg.attach_alternative(mail_data['html'], 'text/html')
            msg.send()
        return

    @staticmethod
    def debug_email(model, subject, message, email_from, recipients, notification_type):
        MailHelper.debug_count += 1
        """
        Mock de envío para utilizar en desarrollo, crea un documento con los datos del email a enviar
        """
        from django.utils.encoding import smart_str, smart_unicode
        import sys
        import time

        sys.stdout.softspace = 0
        nombrearchivo = PROJECT_ROOT + '/tmp/debug_emails/' + str(int(time.time())) + '-' + str(MailHelper.debug_count) + '-' + notification_type + '.txt'
        print nombrearchivo
        f = open(nombrearchivo, 'w')
        print >>f, u"Subject:", subject.encode('utf8')
        print >>f, u"Message:", message.encode('utf8')
        print >>f, u"From:", email_from.encode('utf8')
        print >>f, u"Recipients:", recipients
        print >>f, u"Notification type:", notification_type.encode('utf8')
        print >>f, u"Model:", model

    """

    Mails para los establecimientos

    """
    @staticmethod
    def establecimiento_create(establecimiento):
        recipients = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        return {
            'subject': u'Solicitud de Registro de nueva Unidad Educativa',
            'message': u"""Estimado/a

Se ha solicitado el registro de una nueva Unidad Educativa cuyos datos son:

Tipo: Sede
Fecha de Solicitud: """ + datetime.date.today().strftime("%d/%m/%Y") + u"""
Usuario que Solicita el Alta: """ + get_current_user().apellido + ", " + get_current_user().nombre +  u"""
Jurisdicción: """ + unicode(establecimiento.dependencia_funcional.jurisdiccion) + u"""
Dependencia Funcional: """ + unicode(establecimiento.dependencia_funcional) + u"""
CUE: """ + establecimiento.cue + u"""
Nombre de la Unidad Educativa: """ + establecimiento.nombre + u"""

Recuerde que la Unidad Educativa permanecerá en estado Pendiente hasta tanto sea Registrada.

Se requiere su intervención para cambiar el estado. Si desea hacerlo ahora, por favor ingrese a http://reffod.infd.edu.ar


Correo Automático - Sistema REFFOD
Instituto Nacional de Formación Docente
""",
            'html': u"""Estimado/a
<br /><br />
Se ha solicitado el <b>registro de una nueva Unidad Educativa</b> cuyos datos son:
<br /><br />
Tipo: <b>Sede</b><br />
Fecha de Solicitud: <b>""" + datetime.date.today().strftime("%d/%m/%Y") + u"""</b><br />
Usuario que Solicita el Alta: <b>""" + get_current_user().apellido + ", " + get_current_user().nombre +  u"""</b><br />
Jurisdicción: <b>""" + unicode(establecimiento.dependencia_funcional.jurisdiccion) + u"""</b><br />
Dependencia Funcional: <b>""" + unicode(establecimiento.dependencia_funcional) + u"""</b><br />
CUE: <b>""" + establecimiento.cue + u"""</b><br />
Nombre de la Unidad Educativa: <b>""" + establecimiento.nombre + u"""</b><br />
<br /><br />
Recuerde que la Unidad Educativa permanecerá en estado <b>Pendiente</b> hasta tanto sea <b>Registrada</b>.
<br /><br />
Se requiere su intervención para cambiar el estado. Si desea hacerlo ahora, por favor ingrese a <a href="http://reffod.infd.edu.ar">http://reffod.infd.edu.ar</a>
<br /><br />
<b>
Correo Automático - Sistema REFFOD<br />
Instituto Nacional de Formación Docente<br />
</b>
""",
            'recipients': recipients,
        }
        
    @staticmethod
    def establecimiento_update(establecimiento):
        return {
            'subject': u'Actualización de datos de establecimiento',
            'message': u'Se ha modificado el establecimiento',
            'email_from': u'pepe@example.com',
            #'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
            'recipients': []
        }

    @staticmethod
    def establecimiento_delete(establecimiento):
        return {
            'subject': u'Baja de establecimiento',
            'message': u'Se ha dado de baja el establecimiento',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        }

    """

    Mails para los anexos

    """
    @staticmethod
    def anexo_create(anexo):
        recipients = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        return {
            'subject': u'Solicitud de registro de nuevo anexo',
            'message': u"""Estimado/a

Se ha solicitado el registro de una nueva Unidad Educativa cuyos datos son:

Tipo: Anexo
Fecha de Solicitud: """ + datetime.date.today().strftime("%d/%m/%Y") + u"""
Usuario que Solicita el Alta: """ + get_current_user().apellido + ", " + get_current_user().nombre +  u"""
Jurisdicción: """ + unicode(anexo.establecimiento.dependencia_funcional.jurisdiccion) + u"""
Dependencia Funcional: """ + unicode(anexo.establecimiento.dependencia_funcional) + u"""
CUE: """ + anexo.cue + u"""
Nombre de la Unidad Educativa: """ + anexo.nombre + u"""

Recuerde que la Unidad Educativa permanecerá en estado Pendiente hasta tanto sea Registrada.

Se requiere su intervención para cambiar el estado. Si desea hacerlo ahora, por favor ingrese a http://reffod.infd.edu.ar


Correo Automático - Sistema REFFOD
Instituto Nacional de Formación Docente
""",
            'html': u"""Estimado/a
<br /><br />
Se ha solicitado el <b>registro de una nueva Unidad Educativa</b> cuyos datos son:
<br /><br />
Tipo: <b>Anexo</b><br />
Fecha de Solicitud: <b>""" + datetime.date.today().strftime("%d/%m/%Y") + u"""</b><br />
Usuario que Solicita el Alta: <b>""" + get_current_user().apellido + ", " + get_current_user().nombre +  u"""</b><br />
Jurisdicción: <b>""" + unicode(anexo.establecimiento.dependencia_funcional.jurisdiccion) + u"""</b><br />
Dependencia Funcional: <b>""" + unicode(anexo.establecimiento.dependencia_funcional) + u"""</b><br />
CUE: <b>""" + anexo.cue + u"""</b><br />
Nombre de la Unidad Educativa: <b>""" + anexo.nombre + u"""</b><br />
<br /><br />
Recuerde que la Unidad Educativa permanecerá en estado <b>Pendiente</b> hasta tanto sea <b>Registrada</b>.
<br /><br />
Se requiere su intervención para cambiar el estado. Si desea hacerlo ahora, por favor ingrese a <a href="http://reffod.infd.edu.ar">http://reffod.infd.edu.ar</a>
<br /><br />
<b>
Correo Automático - Sistema REFFOD<br />
Instituto Nacional de Formación Docente<br />
</b>
""",
            'recipients': recipients,
        }

    @staticmethod
    def anexo_update(anexo):
        return {
            'subject': u'Actualización de datos de anexo',
            'message': u'Se ha modificado el anexo',
            'email_from': u'pepe@example.com',
            #'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
            'recipients': []
        }

    @staticmethod
    def anexo_delete(anexo):
        return {
            'subject': u'Baja de anexo',
            'message': u'Se ha dado de baja el anexo',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        }

    """

    Mails para las extensiones áulicas

    """
    @staticmethod
    def extension_aulica_create(extension_aulica):
        recipients = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        return {
            'subject': u'Solicitud de registro de nueva extensión áulica',
            'message': u"""Estimado/a

Se ha solicitado el registro de una nueva Unidad Educativa cuyos datos son:

Tipo: Extensión Aulica
Fecha de Solicitud: """ + datetime.date.today().strftime("%d/%m/%Y") + u"""
Usuario que Solicita el Alta: """ + get_current_user().apellido + ", " + get_current_user().nombre +  u"""
Jurisdicción: """ + unicode(extension_aulica.establecimiento.dependencia_funcional.jurisdiccion) + u"""
Dependencia Funcional: """ + unicode(extension_aulica.establecimiento.dependencia_funcional) + u"""
CUE: """ + extension_aulica.cue + u"""
Nombre de la Unidad Educativa: """ + extension_aulica.nombre + u"""

Recuerde que la Unidad Educativa permanecerá en estado Pendiente hasta tanto sea Registrada.

Se requiere su intervención para cambiar el estado. Si desea hacerlo ahora, por favor ingrese a http://reffod.infd.edu.ar


Correo Automático - Sistema REFFOD
Instituto Nacional de Formación Docente
""",
            'html': u"""Estimado/a
<br /><br />
Se ha solicitado el <b>registro de una nueva Unidad Educativa</b> cuyos datos son:
<br /><br />
Tipo: <b>Extensión Aulica</b><br />
Fecha de Solicitud: <b>""" + datetime.date.today().strftime("%d/%m/%Y") + u"""</b><br />
Usuario que Solicita el Alta: <b>""" + get_current_user().apellido + ", " + get_current_user().nombre +  u"""</b><br />
Jurisdicción: <b>""" + unicode(extension_aulica.establecimiento.dependencia_funcional.jurisdiccion) + u"""</b><br />
Dependencia Funcional: <b>""" + unicode(extension_aulica.establecimiento.dependencia_funcional) + u"""</b><br />
CUE: <b>""" + extension_aulica.cue + u"""</b><br />
Nombre de la Unidad Educativa: <b>""" + extension_aulica.nombre + u"""</b><br />
<br /><br />
Recuerde que la Unidad Educativa permanecerá en estado <b>Pendiente</b> hasta tanto sea <b>Registrada</b>.
<br /><br />
Se requiere su intervención para cambiar el estado. Si desea hacerlo ahora, por favor ingrese a <a href="http://reffod.infd.edu.ar">http://reffod.infd.edu.ar</a>
<br /><br />
<b>
Correo Automático - Sistema REFFOD<br />
Instituto Nacional de Formación Docente<br />
</b>
""",
            'recipients': recipients,
        }

    @staticmethod
    def extension_aulica_update(extension_aulica):
        return {
            'subject': u'Actualizació de datos de extensión áulica',
            'message': u'Se ha modificado la extensión áulica',
            'email_from': u'pepe@example.com',
            #'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
            'recipients': []
        }

    @staticmethod
    def extension_aulica_delete(extension_aulica):
        return {
            'subject': u'Baja de extensión áulica',
            'message': u'Se ha dado de baja la extensión áulica',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        }

    """
    Mails para los títulos
    """
    @staticmethod
    def titulo_create(titulo):
        return {
            'subject': u'Creación de título',
            'message': u'Se ha creado un nuevo título',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        }

    @staticmethod
    def titulo_update(titulo):
        return {
            'subject': u'Actualización de datos de título',
            'message': u'Se ha modificado el título',
            'email_from': u'pepe@example.com',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        }

    @staticmethod
    def titulo_delete(titulo):
        return {
            'subject': u'Baja de título',
            'message': u'Se ha dado de baja el título',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_ADMIN_NACIONAL)]
        }

    @staticmethod
    def certificacion_carga_establecimiento(certificacion):
        usuario = u'' + certificacion.usuario.apellido + ' ' + certificacion.usuario.nombre
        establecimiento = certificacion.establecimiento
        anio = str(certificacion.anio)
        ambito_dependencia_funcional_id = establecimiento.dependencia_funcional.ambito.id
        ambito_jurisdiccion_id = establecimiento.dependencia_funcional.jurisdiccion.ambito.id
        recipientes = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_REFERENTE_JURISDICCIONAL).filter(perfiles__ambito__id__in=[ambito_jurisdiccion_id, ambito_dependencia_funcional_id]).distinct()]
        return {
            'subject': u'Certificación de Carga ' + anio,
            'message': u'El usuario ' + usuario + ' ha certificado la carga de datos ' + anio + ' para el establecimiento ' + unicode(establecimiento) + '. Por favor chequee que todos los datos hayan sido consignados correctamente.',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': recipientes
        }

    @staticmethod
    def certificacion_carga_anexo(certificacion):
        usuario = certificacion.usuario.apellido + ' ' + certificacion.usuario.nombre
        anexo = certificacion.anexo
        anio = str(certificacion.anio)
        ambito_dependencia_funcional_id = anexo.establecimiento.dependencia_funcional.ambito.id
        ambito_jurisdiccion_id = anexo.establecimiento.dependencia_funcional.jurisdiccion.ambito.id
        recipientes = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_REFERENTE_JURISDICCIONAL).filter(perfiles__ambito__id__in=[ambito_jurisdiccion_id, ambito_dependencia_funcional_id]).distinct()]
        return {
            'subject': u'Certificación de Carga ' + anio,
            'message': u'El usuario ' + usuario + ' ha certificado la carga de datos ' + anio + ' para el anexo ' + unicode(anexo) + '. Por favor chequee que todos los datos hayan sido consignados correctamente.',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': recipientes
        }

    @staticmethod
    def certificacion_carga_extension_aulica(certificacion):
        usuario = certificacion.usuario.apellido + ' ' + certificacion.usuario.nombre
        extension_aulica = certificacion.extension_aulica
        anio = str(certificacion.anio)
        ambito_dependencia_funcional_id = extension_aulica.establecimiento.dependencia_funcional.ambito.id
        ambito_jurisdiccion_id = extension_aulica.establecimiento.dependencia_funcional.jurisdiccion.ambito.id
        recipientes = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_REFERENTE_JURISDICCIONAL).filter(perfiles__ambito__id__in=[ambito_jurisdiccion_id, ambito_dependencia_funcional_id]).distinct()]
        return {
            'subject': u'Certificación de Carga ' + anio,
            'message': u'El usuario ' + usuario + ' ha certificado la carga de datos ' + anio + u' para la extensión áulica ' + unicode(extension_aulica) + '. Por favor chequee que todos los datos hayan sido consignados correctamente.',
            #'recipients': ['user@example.com', 'admin@example.com'],
            'recipients': recipientes
        }

    @staticmethod
    def numeracion_solicitud(validez):
        from apps.validez_nacional.models.ValidezNacional import ValidezNacional
        solicitud = validez.solicitud
        ue = validez.get_unidad_educativa()
        
        if validez.tipo_unidad_educativa == ValidezNacional.TIPO_UE_SEDE:
            establecimiento = validez.get_establecimiento()
            
        else:
            establecimiento = validez.get_anexo().establecimiento
            
        ambito_dependencia_funcional_id = establecimiento.dependencia_funcional.ambito.id
        ambito_jurisdiccion_id = establecimiento.dependencia_funcional.jurisdiccion.ambito.id
        if validez.dictamen_cofev is None:
            dictamen_cofev = ''
        else:
            dictamen_cofev = validez.dictamen_cofev
        recipientes = [u.email for u in MailHelper.get_usuarios_activos_por_rol(Rol.ROL_REFERENTE_JURISDICCIONAL).filter(perfiles__ambito__id__in=[ambito_jurisdiccion_id, ambito_dependencia_funcional_id]).distinct()]
        return {
            'subject': u'Nuevo registro de Validez Nacional',
            'message': u"""Estimado/a

Se ha registrado una nueva numeración de título nacional, cuyos datos son:

Tipo: """ + validez.tipo_unidad_educativa + u"""
CUE: """ + ue.cue + u"""
Jurisdicción: """ + solicitud.jurisdiccion.nombre + u"""
Carrera: """ + validez.carrera + u"""
Título: """ + validez.titulo_nacional + u"""
Primera Cohorte Autorizada: """ + str(validez.primera_cohorte) + u"""
Últimas Cohorte Autorizada: """ + str(validez.ultima_cohorte) + u"""
Dictamen de la CoFEv: """ + dictamen_cofev + u"""
Normativa Jurisdiccional: """ + validez.normativa_jurisdiccional + u"""
Normativa Nacional: """ + validez.normativas_nacionales + u"""

Correo Automático - Sistema REFFOD
Instituto Nacional de Formación Docente
""",
            'html': u"""Estimado/a
<br /><br />
Se ha registrado una nueva numeración de título nacional, cuyos datos son::
<br /><br />
Tipo: <b>""" + validez.tipo_unidad_educativa + u"""</b><br />
Jurisdicción: <b>""" + solicitud.jurisdiccion.nombre + u"""</b><br />
CUE: <b>""" + ue.cue + u"""</b><br />
Carrera: <b>""" + validez.carrera + u"""
Título: <b>""" + validez.titulo_nacional + u"""</b><br />
Primera Cohorte Autorizada: <b>""" + str(validez.primera_cohorte) + u"""</b><br />
Últimas Cohorte Autorizada: <b>""" + str(validez.ultima_cohorte) + u"""</b><br />
Dictamen de la CoFEv: <b>""" + dictamen_cofev + u"""</b><br />
Normativa Jurisdiccional: <b>""" + validez.normativa_jurisdiccional + u"""</b><br />
Normativa Nacional: <b>""" + validez.normativas_nacionales + u"""</b><br />
<br /><br />
<b>
Correo Automático - Sistema REFFOD<br />
Instituto Nacional de Formación Docente<br />
</b>
""",
            'recipients': recipientes,
        }
