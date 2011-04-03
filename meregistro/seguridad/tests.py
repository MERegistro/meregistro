# -*- coding: UTF-8 -*-

from django.test import TestCase

class UsuarioCreateFormTest(TestCase):
  """
  Tests para el form de alta de usuario: UsuarioCreateForm.
  """
  def test_usuario_create_contrasenyas_coinciden(self):
    from seguridad.forms import UsuarioCreateForm
    form = UsuarioCreateForm({'password': '1234', 'repeat_password': '123'})
    self.failUnless(form.errors.has_key('password'), 'No se seteo error para campo password')
    self.failUnless("no coinciden" in form.errors['password'].as_text(), 'El error no indica que las contraseñas no coinciden')


def login(client, tipo_documento_id, documento, password):
  """
  Inicia sesion para un Client de test usando el usuario y contraseña
  pasados por parametro.
  """
  return client.post('/login', {'tipo_documento': tipo_documento_id, 'documento': documento, 'password': password})

def loginAsAdmin(client):
  return login(client, 1, 'test', 'test')

class BloqueoUsuarioTest(TestCase):
  """
  Tests para la funcionalidad de bloqueo/desbloqueo de usuario.
  """
  fixtures = ['data_tests.yaml']
  def setUp(self):
    from seguridad.models import Usuario, TipoDocumento
    self.usuario = Usuario.objects.create(
      tipo_documento=TipoDocumento.objects.get(pk=1),
      documento='12345678',
      apellido='usr',
      nombre='usr',
      email='usr@example.org',
      is_active=True
    )
    self.usuario.set_password('usr')
    self.usuario.save()

  def test_bloquear_usuario(self):
    from django.test.client import Client
    from seguridad.models import Usuario
    c = Client()
    loginAsAdmin(c)
    response = c.get('/seguridad/usuario/' + str(self.usuario.id) + '/bloquear')
    self.failUnlessEqual(response.status_code, 200, 'View inexistente')
    response = c.post('/seguridad/usuario/' + str(self.usuario.id) + '/bloquear')
    self.failUnlessEqual(response.status_code, 302, 'No redirecciono a edicion de usuario')
    self.usuario = Usuario.objects.get(pk=self.usuario.id)
    self.failIf(self.usuario.is_active, 'Usuario no bloqueado')
    response = login(c, self.usuario.tipo_documento.id, self.usuario.documento, 'usr')
    self.failIf(response.status_code == 302, 'Usuario bloqueado no deberia iniciar sesion')
