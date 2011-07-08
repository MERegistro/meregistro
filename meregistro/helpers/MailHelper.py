# -*- coding: utf-8 -*-
from django.db import models
from django.core.mail import send_mail
from settings import DEBUG, PROJECT_ROOT


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

    UNIDAD_EXTENSION_CREATE = u'UnidadExtensionCreate'
    UNIDAD_EXTENSION_UPDATE = u'UnidadExtensionUpdate'
    UNIDAD_EXTENSION_DELETE = u'UnidadExtensionDelete'

    TITULO_CREATE = u'TituloCreate'
    TITULO_UPDATE = u'TituloUpdate'
    TITULO_DELETE = u'TituloDelete'

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
            MailHelper.UNIDAD_EXTENSION_CREATE: MailHelper.unidad_extension_create,
            MailHelper.UNIDAD_EXTENSION_UPDATE: MailHelper.unidad_extension_update,
            MailHelper.UNIDAD_EXTENSION_DELETE: MailHelper.unidad_extension_delete,
            MailHelper.TITULO_CREATE: MailHelper.titulo_create,
            MailHelper.TITULO_UPDATE: MailHelper.titulo_update,
            MailHelper.TITULO_DELETE: MailHelper.titulo_delete,

        }
        """ EJ:  mail_data = MailHelper.establecimiento_create(model) """
        mail_data = mail_data_call_dict[notification_type](model)

        try:
            email_from = mail_data['email_from']
        except KeyError:
            email_from = MailHelper.EMAIL_FROM_DEFAULT

        """
        if DEBUG:
            MailHelper.debug_email(model, mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], notification_type)
        else:
            send_mail(mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], fail_silently=False)
        """
        return

    @staticmethod
    def debug_email(model, subject, message, email_from, recipients, notification_type):
        """
        Mock de envío para utilizar en desarrollo, crea un documento con los datos del email a enviar
        """
        from django.utils.encoding import smart_str, smart_unicode
        import sys
        import time

        sys.stdout.softspace = 0
        f = open(PROJECT_ROOT + '/tmp/debug_emails/' + str(int(time.time())) + '-' + notification_type + '.txt', 'w')
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
        return {
            'subject': u'Creación de establecimiento',
            'message': u'Se ha creado un nuevo establecimiento',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }
    @staticmethod
    def establecimiento_update(establecimiento):
        return {
            'subject': u'Actualizacióm de datos de establecimiento',
            'message': u'Se ha modificado el establecimiento',
            'email_from': u'pepe@example.com',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def establecimiento_delete(establecimiento):
        return {
            'subject': u'Baja de establecimiento',
            'message': u'Se ha dado de baja el establecimiento',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    """

    Mails para los anexos

    """
    @staticmethod
    def anexo_create(anexo):
        return {
            'subject': u'Creación de anexo',
            'message': u'Se ha creado un nuevo anexo',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }

    @staticmethod
    def anexo_update(anexo):
        return {
            'subject': u'Actualizacióm de datos de anexo',
            'message': u'Se ha modificado el anexo',
            'email_from': u'pepe@example.com',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def anexo_delete(anexo):
        return {
            'subject': u'Baja de anexo',
            'message': u'Se ha dado de baja el anexo',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    """

    Mails para las unidades de extensión

    """
    @staticmethod
    def unidad_extension_create(unidad_extension):
        return {
            'subject': u'Creación de unidad de extensión',
            'message': u'Se ha creado una nueva unidad de extensión',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }

    @staticmethod
    def unidad_extension_update(unidad_extension):
        return {
            'subject': u'Actualizacióm de datos de unidad de extensión',
            'message': u'Se ha modificado la unidad de extensión',
            'email_from': u'pepe@example.com',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def unidad_extension_delete(unidad_extension):
        return {
            'subject': u'Baja de unidad de extensión',
            'message': u'Se ha dado de baja la unidad de extensión',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    """

    Mails para los títulos

    """
    @staticmethod
    def titulo_create(titulo):
        return {
            'subject': u'Creación de título',
            'message': u'Se ha creado un nuevo título',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }

    @staticmethod
    def titulo_update(titulo):
        return {
            'subject': u'Actualizacióm de datos de título',
            'message': u'Se ha modificado el título',
            'email_from': u'pepe@example.com',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def titulo_delete(titulo):
        return {
            'subject': u'Baja de título',
            'message': u'Se ha dado de baja el título',
            'recipients': ['user@example.com', 'admin@example.com'],
        }
