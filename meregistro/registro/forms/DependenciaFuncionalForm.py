from django.forms import ModelForm
from registro.models import DependenciaFuncional

class DependenciaFuncionalForm(ModelForm):

	class Meta:
		model = DependenciaFuncional
