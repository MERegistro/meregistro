from django.forms import ModelForm
from django import forms
from apps.seguridad.models import Rol, Credencial


class RolForm(ModelForm):
    credenciales = forms.ModelMultipleChoiceField(queryset=Credencial.objects.all().order_by('descripcion'), widget=forms.CheckboxSelectMultiple, required=False)
    roles_asignables = forms.ModelMultipleChoiceField(queryset=Rol.objects.all().order_by('descripcion'), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Rol

    def __unicode__(self):
        return self.descripcion
