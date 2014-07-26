import json

from json_schema_validator.schema import Schema
from json_schema_validator.validator import Validator
from json_schema_validator.errors import ValidationError


def validate_against_schema(schema_name="release-schema", raw_data=""):
    status = 'success'
    error = None

    schema = Schema(json.load(open("validator/schemas/%s.json" % schema_name)))

    try:
        data = json.loads(raw_data)
    except ValueError, e:
        status = 'input-error'
        error = e
        return status, error
    
    try:
        Validator.validate(schema, data)
    except ValidationError, e:
        status = 'validation-error'
        error = e
        return status, error

    return status, error
