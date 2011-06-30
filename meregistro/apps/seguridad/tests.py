# -*- coding: UTF-8 -*-

from django.test import TestCase
from django.test.client import Client


def login(client, tipo_documento_id, documento, password):
    """
    Inicia sesion para un Client de test usando el usuario y contraseña
    pasados por parametro.
    """
    return client.post('/login', {'tipo_documento': tipo_documento_id, 'documento': documento, 'password': password})


def createClientAs(tipo_documento_id, documento, password):
    """
    Retorna un client logueado con los parametros pasados.
    """
    c = Client()
    login(c, tipo_documento_id, documento, password)
    return c


def createClientAsAdmin():
    """
    Retorna un client logueado como Administrador.
    """
    return createClientAs(1, 'test', 'test')


class UsuarioCreateFormTest(TestCase):
    """
    Tests para el form de alta de usuario: UsuarioCreateForm.
    """
    def test_usuario_create_contrasenyas_coinciden(self):
        from apps.seguridad.forms import UsuarioCreateForm

        form = UsuarioCreateForm({'password': '1234', 'repeat_password': '123'})
        self.failUnless(form.errors.has_key('password'), 'No se seteo error para campo password')
        self.failUnless("no coinciden" in form.errors['password'].as_text(), 'El error no indica que las contraseñas no coinciden')


class BloqueoUsuarioTest(TestCase):
    """
    Tests para la funcionalidad de bloqueo/desbloqueo de usuario.
    """
    fixtures = ['data_tests.yaml']

    def test_bloquear_usuario(self):
        c = createClientAsAdmin()
        # Comienza con un usuario activo.
        from apps.seguridad.models import Usuario
        usuario = Usuario.objects.get(documento='usractivo')
        self.failUnless(usuario.is_active, 'Usuario inactivo')
        # Acceder a la pantalla de bloqueo.
        response = c.get('/seguridad/usuario/' + str(usuario.id) + '/bloquear')
        self.failUnlessEqual(response.status_code, 200, 'View inexistente')
        # Ejecutar la accion de bloqueo.
        response = c.post('/seguridad/usuario/' + str(usuario.id) + '/bloquear', {'motivo': 1})
        self.failUnlessEqual(response.status_code, 302, 'No redirecciono a edicion de usuario')
        # Chequear que se haya guardado el bloqueo.
        usuario = Usuario.objects.get(pk=usuario.id)
        self.failIf(usuario.is_active, 'Usuario no bloqueado')
        # Chequear que el usuario bloqueado no pueda iniciar sesion.
        clientNoLogueado = Client()
        response = login(clientNoLogueado, usuario.tipo_documento.id, usuario.documento, 'test')
        self.failIf(response.status_code == 302, 'Usuario bloqueado no deberia iniciar sesion')

    def test_desbloquear_usuario(self):
        c = createClientAsAdmin()
        # Comienza con un usuario inactivo.
        from apps.seguridad.models import Usuario
        usuario = Usuario.objects.get(documento='usrinactivo')
        self.failIf(usuario.is_active, 'Usuario activo')
        # Acceder a la pantalla de desbloqueo.
        response = c.get('/seguridad/usuario/' + str(usuario.id) + '/desbloquear')
        self.failUnlessEqual(response.status_code, 200, 'View inexistente')
        # Ejecutar la accion de desbloqueo.
        response = c.post('/seguridad/usuario/' + str(usuario.id) + '/desbloquear', {'motivo': 3})
        self.failUnlessEqual(response.status_code, 302, 'No redirecciono a edicion de usuario')
        # Chequear que se haya guardado el desbloqueo.
        usuario = Usuario.objects.get(pk=usuario.id)
        self.failUnless(usuario.is_active, 'Usuario no desbloqueado')
        # Chequear que el usuario desbloqueado pueda iniciar sesion.
        clientNoLogueado = Client()
        response = login(clientNoLogueado, usuario.tipo_documento.id, usuario.documento, 'test')
        self.failUnless(response.status_code == 302, 'Usuario desbloqueado deberia poder iniciar sesion')
