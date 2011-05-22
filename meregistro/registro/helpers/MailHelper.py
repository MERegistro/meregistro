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

    @staticmethod
    def notify_by_email(notification_type=None, model=None):
        """
        Funcionalidad básica de notificación
        """
        if notification_type is None:
            return """ Refactorizar...someday """
        elif notification_type == MailHelper.ESTABLECIMIENTO_CREATE:
            mail_data = MailHelper.establecimiento_create(model)
        elif notification_type == MailHelper.ESTABLECIMIENTO_UPDATE:
            mail_data = MailHelper.establecimiento_update(model)
        elif notification_type == MailHelper.ESTABLECIMIENTO_DELETE:
            mail_data = MailHelper.establecimiento_delete(model)
        elif notification_type == MailHelper.ANEXO_CREATE:
            mail_data = MailHelper.anexo_create(model)
        elif notification_type == MailHelper.ANEXO_UPDATE:
            mail_data = MailHelper.anexo_update(model)
        elif notification_type == MailHelper.ANEXO_DELETE:
            mail_data = MailHelper.anexo_delete(model)

        try:
            email_from = mail_data['email_from']
        except KeyError:
            email_from = MailHelper.EMAIL_FROM_DEFAULT

        if DEBUG:
            MailHelper.debug_email(model, mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], notification_type)
        else:
            send_mail(mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], fail_silently=False)

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

    @staticmethod
    def establecimiento_create(establecimiento):
        """
        Mail para creación de establecimiento
        """
        return {
            'subject': u'Creación de establecimiento',
            'message': u'Se ha creado un nuevo establecimiento',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }

    @staticmethod
    def establecimiento_update(establecimiento):
        """
        Mail para actualización de establecimiento
        """
        return {
            'subject': u'Actualizacióm de datos de establecimiento',
            'message': u'Se ha modificado el establecimiento',
            'email_from': u'pepe@example.com',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def establecimiento_delete(establecimiento):
        """
        Mail para baja de establecimiento
        """
        return {
            'subject': u'Baja de establecimiento',
            'message': u'Se ha dado de baja el establecimiento',
            'recipients': ['user@example.com', 'admin@example.com'],
        }

    @staticmethod
    def anexo_create(anexo):
        """
        Mail para creación de anexo
        """
        return {
            'subject': u'Creación de anexo',
            'message': u'Se ha creado un nuevo anexo',
            'recipients': [u'user@example.com', u'admin@example.com'],
        }
