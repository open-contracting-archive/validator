# -*- coding: utf-8 -*-
import pytest
from mock import patch
from py.path import local

from validator.views import TextFormValidatorView


@pytest.mark.client
def test_form_text_input(rf, client):
    response = client.post('/', {'content': '{"data": []}'})
    assert 'Validation results' in response.content, "Form didn't validate"


def test_form_invalid_json(rf):
    request = rf.post('/', {'content': '{invalid json;'})
    view = TextFormValidatorView.as_view()
    response = view(request)
    assert 'Invalid JSON Input' in response.content, "Form didn't raise invalid JSON error"


def test_form_valid_input(rf):
    request = rf.post('/', {'content': open(local(__file__).dirname + '/assets/simple_example.json').read()})
    view = TextFormValidatorView.as_view()
    response = view(request)
    assert 'Successfully Validated Input JSON' in response.content


def test_form_upload_file(rf):
    with open(local(__file__).dirname + '/assets/simple_example.json') as fp:
        request = rf.post('/', {'file': fp})
    view = TextFormValidatorView.as_view()
    response = view(request)
    assert 'Successfully Validated Input JSON' in response.content


def test_form_remote_url_success(rf):
    with patch('validator.views.requests') as mock_requests:
        mock_response = mock_requests.get.return_value
        mock_response.status_code = 200
        mock_response.content = '{{{'

        request = rf.post('/', {'url': 'http://data.example.com/invalid.json'})

        view = TextFormValidatorView.as_view()
        response = view(request)

        assert 'Invalid JSON Input' in response.content, "Requests didn't process remote URL"


# The test doesn't correctly mock requests.status_code so raise_for_status() does not
# raise correctly and it fails.
@pytest.mark.xfail
def test_form_remote_url_not_found(rf):
    with patch('validator.views.requests') as mock_requests:
        mock_response = mock_requests.get.return_value
        mock_response.status_code = 404
        mock_response.reason = '404 Client Error: File not found'
        mock_response.content = None

        request = rf.post('/', {'url': 'http://data.example.com/404.json'})

        view = TextFormValidatorView.as_view()
        response = view(request)

        assert 'Error retrieving URL' in response.content, "Requests didn't fail on remote 404"


def test_upload_gzip_file(rf):
    with open(local(__file__).dirname + '/assets/simple_example.json.gz') as fp:
        request = rf.post('/', {'file': fp})
    view = TextFormValidatorView.as_view()
    response = view(request)
    assert 'Successfully Validated Input JSON' in response.content, 'Gzipped filed did not validate'


def test_upload_gzip_file_partial_file(rf):
    with open(local(__file__).dirname + '/assets/simple_example_partial_file.json.gz') as fp:
        request = rf.post('/', {'file': fp})
    view = TextFormValidatorView.as_view()
    response = view(request)
    assert 'Error reading the file' in response.content, 'Broken gzip file didn not fail'
