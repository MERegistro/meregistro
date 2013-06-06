from django.forms import ModelForm
from django import forms
from apps.seguridad.models import Rol, Credencial, TipoAmbito


class RolForm(ModelForm):
    credenciales = forms.ModelMultipleChoiceField(queryset=Credencial.objects.all().order_by('descripcion'), widget=forms.CheckboxSelectMultiple, required=False)
    roles_asignables = forms.ModelMultipleChoiceField(queryset=Rol.objects.all().order_by('descripcion'), widget=forms.CheckboxSelectMultiple, required=False)
    tipos_ambito_asignable = forms.ModelMultipleChoiceField(queryset=TipoAmbito.objects.all().order_by('descripcion'), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Rol
        exclude = ['path']

    def __unicode__(self):
        return self.descripcion

    def __init__(self, *args, **kw):
        ModelForm.__init__(self, *args, **kw)
        if kw.has_key('instance'):
            self.fields['padre'].queryset = Rol.objects.exclude(id=kw['instance'].id).order_by('descripcion')
        
