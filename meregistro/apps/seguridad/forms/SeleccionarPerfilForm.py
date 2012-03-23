# -*- coding: UTF-8 -*-

from django import forms
from apps.seguridad.models import Perfil


class SeleccionarPerfilForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        self.base_fields['perfil'] = forms.ChoiceField(label='Perfil',
            choices=[(p.id, p.rol.descripcion + ' (' + p.ambito.descripcion + ')') for p in user.perfiles.exclude(fecha_desasignacion__isnull=False).order_by('rol__descripcion', 'ambito__descripcion')])
        forms.Form.__init__(self, *args, **kwargs)

    def clean_perfil(self):
        '''
        Chequea que el perfil seleccionador pertenezca al usuario
        '''

        perfil_id = self.cleaned_data['perfil']
        try:
            perfil = Perfil.objects.get(pk=perfil_id)
        except Perfil.DoesNotExist:
            raise forms.ValidationError(u'Perfil inexistente')
        if perfil.usuario.id != self.user.id:
            raise forms.ValidationError(u'Perfil invalido')
        return perfil_id
