# -*- coding: utf-8 -*-
from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Field, HTML
from crispy_forms.bootstrap import InlineRadios


class TextValidatorForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, required=False)
    file = forms.FileField(required=False)
    url = forms.URLField(required=False)
    schema = forms.ChoiceField([('release-package-schema', 'Release'),
                                ('record-package-schema', 'Record')], error_messages={'required': 'Please select which type of schema you wish to validate'})

    def __init__(self, *args, **kwargs):
        super(TextValidatorForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = '.'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        Div(HTML("<p>Submit the data through <strong>File</strong>, <strong>URL</strong> or <strong>Content</strong>. Only one input type at time will be validated.</p>")),
                        Div(Field('file')),
                        Div(Field('url')),
                        Div(Field('content')),
                        css_class="panel-body"
                    ),
                    css_class="panel panel-default",
                ),
                Div(InlineRadios('schema')),
                Div(Submit('submit', 'Submit')),
                css_class="col-md-12"
            )
        )

    def clean(self):
        cleaned_data = super(TextValidatorForm, self).clean()
        if not (cleaned_data.get('content') or cleaned_data.get('file') or cleaned_data.get('url')):
            raise forms.ValidationError('At least one input type is required', code='missing-input')

        return cleaned_data
