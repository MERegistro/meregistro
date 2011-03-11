# -*- coding: UTF-8 -*-

from django import forms
from seguridad.models import TipoDocumento

class LoginForm(forms.Form):
  tipo_documento_choices = [(t.id, t.descripcion) for t in TipoDocumento.objects.all()]
  tipo_documento = forms.ChoiceField(label='Tipo de documento', choices=tipo_documento_choices)
  
  documento = forms.CharField(max_length=20, label='documento')
  password = forms.CharField(widget=forms.PasswordInput(render_value=False), label='contraseña')


