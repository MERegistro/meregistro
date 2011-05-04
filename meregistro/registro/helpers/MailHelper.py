# -*- coding: utf-8 -*-
from django.db import models
from django.core.mail import send_mail
from settings import DEBUG, PROJECT_ROOT
"""
Wrapper para envío de emails del sistema
"""
class MailHelper():
	EMAIL_FROM_DEFAULT = u'admin@example.com'

	ESTABLECIMIENTO_CREATE = u'EstablecimientoCreate'
	ESTABLECIMIENTO_UPDATE = u'EstablecimientoUpdate'

	"""
	Funcionalidad básica de notificación
	"""
	@staticmethod
	def notify_by_email(notification_type = None, model = None):
		if notification_type is None:
			return
		elif notification_type == MailHelper.ESTABLECIMIENTO_CREATE:
			mail_data = MailHelper.establecimiento_create(model)
		elif notification_type == MailHelper.ESTABLECIMIENTO_UPDATE:
			mail_data = MailHelper.establecimiento_update(model)

		try:
			email_from = mail_data['email_from']
		except KeyError:
			email_from = MailHelper.EMAIL_FROM_DEFAULT

		if DEBUG:
			MailHelper.debug_email(model, mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], notification_type)
		else:
			send_mail(mail_data['subject'], mail_data['message'], email_from, mail_data['recipients'], fail_silently = False)

	"""
	Mock de envío para utilizar en desarrollo, crea un documento con los datos del email a enviar
	"""
	@staticmethod
	def debug_email(model, subject, message, email_from, recipients, notification_type):
		from django.utils.encoding import smart_str, smart_unicode
		import sys, time
		sys.stdout.softspace=0
		f = open(PROJECT_ROOT  + '/tmp/debug_emails/' + str(int(time.time())) + '-' + notification_type + '.txt', 'w')
		print >>f, u"Subject:", subject.encode('utf8')
		print >>f, u"Message:", message.encode('utf8')
		print >>f, u"From:", email_from.encode('utf8')
		print >>f, u"Recipients:", recipients
		print >>f, u"Notification type:", notification_type.encode('utf8')
		print >>f, u"Model:", model

	"""
	Mail para creación de establecimiento
	"""
	@staticmethod
	def establecimiento_create(establecimiento):
		return {
			'subject': u'Creación de establecimiento',
			'message': u'Se ha creado un nuevo establecimiento',
			'recipients': [u'user@example.com', u'admin@example.com'],
		}

	"""
	Mail para actualización de establecimiento
	"""
	@staticmethod
	def establecimiento_update(establecimiento):
		return {
			'subject': u'Actualizacióm de datos de establecimiento',
			'message': u'Se ha modificado el establecimiento',
			'email_from': u'pepe@example.com',
			'recipients': ['user@example.com', 'admin@example.com'],
		}
