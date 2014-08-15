# -*- coding: utf-8 -*-
from py.path import local

from validator.utils import validate_against_schema


def test_input_basic():
    raw_data = '{"data": []}'
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert status == 'validation-error', 'Validator failed to raise validation error'


def test_input_broken_json():
    raw_data = '{broken json;'
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert status == 'input-error', 'Validator failed to raise input validation error'


def test_input_valid_json():
    raw_data = open(local(__file__).dirname + '/assets/simple_example.json').read()
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert status == 'input-valid', 'Validator did not validate valid input'


def test_input_invalid_json():
    raw_data = open(local(__file__).dirname + '/assets/invalid_missing_publisher.json').read()
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert status == 'validation-error', 'Validator did not return validation error'
    assert len(error) == 1, 'Validator returned incorrect number of errors'


def test_input_invalid_json_multiple_errors():
    raw_data = open(local(__file__).dirname + '/assets/invalid_multiple_errors.json').read()
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert status == 'validation-error', 'Validator did not return validation error'
    assert len(error) == 3, 'Validator returned incorrect number of errors'


def test_input_release_schema():
    raw_data = open(local(__file__).dirname + '/assets/random_release_example.json').read()
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert 'release-schema.json' in schema.get('id')


def test_input_record_schema():
    raw_data = open(local(__file__).dirname + '/assets/random_record_example.json').read()
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert 'record-schema.json' in schema.get('id')


def test_fallback_to_release_schema():
    raw_data = open(local(__file__).dirname + '/assets/invalid_missing_publisher.json').read()
    status, error, schema = validate_against_schema(raw_data=raw_data)
    assert 'release-schema.json' in schema.get('id')
