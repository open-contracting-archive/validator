# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class TextValidatorForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        super(TextValidatorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Submit'))
