# -*- coding: utf-8 -*-
from validator.utils import validate_against_schema


def test_input_basic():
    raw_data = '{"data": []}'
    status, error = validate_against_schema(raw_data=raw_data)
    assert status == 'validation-error', 'Validator failed to raise validation error'


def test_input_broken_json():
    raw_data = '{broken json;'
    status, error = validate_against_schema(raw_data=raw_data)
    assert status == 'input-error', 'Validator failed to raise input validation error'


def test_input_valid_json():
    raw_data = open('validator/tests/assets/simple_example.json').read()
    status, error = validate_against_schema(raw_data=raw_data)
    assert status == 'input-valid', 'Validator did not validate valid input'


def test_input_invalid_json():
    raw_data = open('validator/tests/assets/invalid_missing_publisher.json').read()
    status, error = validate_against_schema(raw_data=raw_data)
    assert status == 'validation-error', 'Validator did not return validation error'
    assert len(error) == 1, 'Validator returned incorrect number of errors'


def test_input_invalid_json_multiple_errors():
    raw_data = open('validator/tests/assets/invalid_multiple_errors.json').read()
    status, error = validate_against_schema(raw_data=raw_data)
    assert status == 'validation-error', 'Validator did not return validation error'
    assert len(error) == 3, 'Validator returned incorrect number of errors'
