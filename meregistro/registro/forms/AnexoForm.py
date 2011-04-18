from django.forms import ModelForm
from registro.models import Establecimiento, Anexo
from django.core.exceptions import ValidationError
from django import forms
from django.forms.extras.widgets import SelectDateWidget
import datetime

currentYear = datetime.datetime.now().year

class AnexoForm(ModelForm):
	fecha_alta = forms.DateField(initial = datetime.date.today, widget = SelectDateWidget(years = range(1800, currentYear + 5)))

	class Meta:
		model = Anexo

	def clean_cue(self):
		cue = self.cleaned_data['cue']
		try:
			int(cue) > 0
		except ValueError:
			raise ValidationError(u'El CUE tiene que ser mayor que cero.')
		return cue
