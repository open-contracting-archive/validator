# -*- coding: utf-8 -*-
import gzip
import requests
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO


from django.shortcuts import render
from django.views.generic import FormView

from forms import TextValidatorForm
from utils import validate_against_schema


class TextFormValidatorView(FormView):
    form_class = TextValidatorForm
    template_name = "homepage.html"

    def form_valid(self, form):
        content = None
        status = None

        if self.request.FILES.get('file'):
            content = self.request.FILES['file'].read()
        elif form.cleaned_data.get('url'):
            try:
                r = requests.get(form.cleaned_data.get('url'))

                r.raise_for_status()
                content = r.content
            except requests.exceptions.RequestException, e:
                status = 'remote-error'
                error = e
        else:
            content = form.cleaned_data.get('content')

        if content:
            if (content[0].encode("hex") == '1f'):
                buf = StringIO()
                buf.write(content)
                buf.seek(0)

                f = gzip.GzipFile(mode='rb', fileobj=buf)
                try:
                    content = f.read()
                except IOError, e:
                    status = 'io-error'
                    error = e
                finally:
                    f.close()

            if not status:
                status, error = validate_against_schema(raw_data=content)

        return render(self.request, "validation_result.html",
                    {"status": status, "error": error})
