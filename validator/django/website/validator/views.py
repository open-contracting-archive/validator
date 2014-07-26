# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic import FormView

from forms import TextValidatorForm
from utils import validate_against_schema


class TextFormValidatorView(FormView):
    form_class = TextValidatorForm
    template_name = "homepage.html"

    def form_valid(self, form):
        if self.request.FILES.get('file'):
            content = self.request.FILES['file'].read()
        else:
            content = form.cleaned_data.get('content')

        status, error = validate_against_schema(raw_data=content)

        return render(self.request, "validation_result.html",
                    {"status": status, "error": error})
