# -*- coding: UTF-8 -*-

from django import forms

class UsuarioChangePasswordForm(forms.Form):
  password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')
  repeat_password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='Repetir contraseña')

  def clean(self):
    if self.cleaned_data.get('password') != self.cleaned_data.get('repeat_password'):
        self._errors['password'] = self.error_class([u'Las contraseñas no coinciden'])
    return self.cleaned_data
