# -*- coding: utf-8 -*-

#
# Django customization through meta-programming
#

from django import forms


# Change ModelChoiceField default empty_label to "Seleccione..."

ModelChoiceField_old__init = forms.ModelChoiceField.__init__

def ModelChoiceField__init__(self, queryset, empty_label=u"---------", cache_choices=False,
                 required=True, widget=None, label=None, initial=None,
                 help_text=None, to_field_name=None, *args, **kwargs):
    if empty_label == "---------":
        empty_label = "Seleccione..."
    return ModelChoiceField_old__init(self, queryset, empty_label, cache_choices,
                 required, widget, label, initial,
                 help_text, to_field_name, *args, **kwargs)

forms.ModelChoiceField.__init__ = ModelChoiceField__init__



