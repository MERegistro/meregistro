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



