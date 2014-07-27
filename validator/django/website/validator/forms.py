# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field


class TextValidatorForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(required=False)
    url = forms.URLField(required=False)

    def __init__(self, *args, **kwargs):
        super(TextValidatorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Div(
                Div(Div(Field('file')),
                    Div(Field('url')),
                    css_class="col-md-4",),
                Div(Field('content'), css_class="col-md-8"),
                css_class="row"
            ),
            Div(Div(Submit('submit', 'Submit'), css_class="col-md-4 pull-left"), css_class="row")
        )

    def clean(self):
        cleaned_data = super(TextValidatorForm, self).clean()
        if not (cleaned_data.get('content') or cleaned_data.get('file') or cleaned_data.get('url')):
            raise forms.ValidationError('At least one input type is required', code='missing-input')

        return cleaned_data
