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

    EXTENSION_AULICA_CREATE = u'ExtensionAulicaCreate'
    EXTENSION_AULICA_UPDATE = u'ExtensionAulicaUpdate'
    EXTENSION_AULICA_DELETE = u'ExtensionAulicaDelete'

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
            MailHelper.EXTENSION_AULICA_CREATE: MailHelper.extension_aulica_create,
            MailHelper.EXTENSION_AULICA_UPDATE: MailHelper.extension_aulica_update,
            MailHelper.EXTENSION_AULICA_DELETE: MailHelper.extension_aulica_delete,
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

    Mails para las extensiones áulicas

    """
    @staticmethod
    def extension_aulica_create(extension_aulica):
        return {
            'subject': u'Creación de extensión áulica',
            'message': u'Se ha creado una nueva extensión áulica',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }

    @staticmethod
    def extension_aulica_update(extension_aulica):
        return {
            'subject': u'Actualizacióm de datos de extensión áulica',
            'message': u'Se ha modificado la extensión áulica',
            'email_from': u'pepe@example.com',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def extension_aulica_delete(extension_aulica):
        return {
            'subject': u'Baja de extensión áulica',
            'message': u'Se ha dado de baja la extensión áulica',
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
